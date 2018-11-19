# coding=utf-8
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect, render_to_response
from django.core.cache import cache
from .models import UserProfile
from .models import DeclareProfile
import requests

# Create your views here.
class web_authorization(View):

    def get(self, request):
        from wechatconfig import web_get_code, web_get_fan_info,web_get_access_token,web_check_access_token
        code = request.GET.get("code", "")
        if not code:
            return HttpResponse(u"非法访问")
        requests_web_get_access_token_result = requests.get(web_get_access_token+code).json()
        if 'errmsg' in requests_web_get_access_token_result.keys():
            print  requests_web_get_access_token_result['errmsg']
            return HttpResponseRedirect(web_get_code+'snsapi_base#wechat_redirect')
        # if cache.has_key('web_access_token'):
        #     web_access_token = cache.get('web_access_token')
        # else:
        web_access_token = requests_web_get_access_token_result['access_token']
            # cache.set('web_access_token',web_access_token,20*60)
        fan_openid = requests_web_get_access_token_result['openid']
        fan_info = requests.get(web_get_fan_info + '%s&openid=%s&lang=zh_CN' % (web_access_token, fan_openid))
        fan_info.encoding = 'utf-8'
        fan_info = fan_info.json()
        check_openid = UserProfile.objects.filter(openid=fan_info['openid']).first()
        if not check_openid:
            profile = UserProfile()
            profile.openid = fan_info['openid']
            profile.nickname = fan_info['nickname']
            profile.sex = fan_info['sex']
            profile.city = fan_info['city']
            profile.headimgurl = fan_info['headimgurl']
            profile.save()
        request.session['islogin'] = True
        request.session['user_openid'] = fan_info['openid']
        return redirect('/index')
        #当非第一次登陆时，检测用户头像是否发生变化，若变化，则修改头像url。
        # check_headimgurl = UserProfile.objects.filter(headimgurl = fan_info['headimgurl'], openid = fan_info['openid']).first()
        # if not check_headimgurl:
        #     UserProfile.objects.filter(openid = fan_info['openid']).update(headimgurl = fan_info['headimgurl'])
        # response = HttpResponseRedirect('/index/')
        # response.set_cookie('fanid',check_openid.id,3600)
        # # return response
        # response = render_to_response('index.html', {'id': check_openid.id, 'nickname': fan_info['nickname'], 'sex': fan_info['sex'], 'city': fan_info['city'], 'headimgurl': fan_info['headimgurl']})
        # response.set_cookie('fanid', check_openid.id, 3600)
        # return response


    def test(self, request):
        request.session['user_openid'] = 'ozKcL0l3gjCmZrSGKLMMIFvT-9B8'  # 在Django 中一句话搞定
        request.session['islogin'] = True
        return redirect('/index')

    def jugelogin(self, request):
        # return render(request, 'index.html')
        # print request.session.get('islogin')
        if(request.session.get('islogin') == True):
            openid = request.session.get('user_openid')
            # print(openid)
            if openid:
                return {'code': 2000, 'msg': u"登陆成功", 'openid': openid}
            else:
                return {'code': 4001, 'errmsg': u"非法请求"}
        else:
            return {'code': 4000, 'errmsg': u"请先登录"}

    def getindex(self, request):
        result = self.jugelogin(request)
        if 'errmsg' in result.keys():
            return HttpResponse(result['errmsg'])
        else:
            useropenid = result['openid']
            user = UserProfile.objects.filter(openid=useropenid).first()
            if user:
                # print user.nickname, user.sex, user.city, user.headimgurl
                return render(request, 'index.html', {'nickname': user.nickname, 'sex': user.sex, 'city': user.city,
                                                      'headimgurl': user.headimgurl})
            else:
                return HttpResponse(u'用户登录过期，请重新登录')

    def declaration(self,request):
        if request.method == 'GET':
            return render(request, 'userform.html')

        if request.method == 'POST':
            result = self.jugelogin(request)
            if 'errmsg' in result.keys():
                return HttpResponse(result['errmsg'])
            else:
                useropenid = result['openid']
                userid = UserProfile.objects.filter(openid=useropenid).first().userid
                # profile = DeclareProfile(sender_id=userid, towho=request.POST.get('to', ''),
                #                          anonymous=request.POST.get('anonymous', ''),
                #                          image=request.FILES.get('image', ''),
                #                          content=request.POST.get('content', ''))
                profile = DeclareProfile()
                profile.sender_id = userid
                profile.towho=request.POST.get('towho', '')
                profile.anonymous=request.POST.get('anonymous', '')
                img=request.FILES.get('image', '')
                profile.image = img
                profile.content=request.POST.get('content', '')
                profile.save()
            return HttpResponse(u'提交保存成功')
                # try:
                #
                # except:
                #     return HttpResponse(u'用户登录过期，请重新登录')




