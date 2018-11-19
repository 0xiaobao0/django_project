# coding=utf-8
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect, render_to_response
from django.core.cache import cache
from .models import UserProfile
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
        scope = requests_web_get_access_token_result["scope"]
        fan_info = requests.get(web_get_fan_info + '%s&openid=%s&lang=zh_CN' % (web_access_token, fan_openid))
        fan_info.encoding = 'utf-8'
        fan_info = fan_info.json()

        if scope == "snsapi_userinfo":
            # 防止重复保存
            check_openid = UserProfile.objects.filter(openid=fan_info['openid']).first()
            if not check_openid:
                profile = UserProfile()
                profile.openid = fan_info['openid']
                profile.nickname = fan_info['nickname']
                profile.sex = fan_info['sex']
                profile.city = fan_info['city']
                profile.headimgurl = fan_info['headimgurl']
                profile.save()

        # 如果没有数据库中没有检索到该用户的openid，则该用户为第一次登陆，让其跳转到授权页面，
        # 当其点击带有修改后scope的值的按钮后，再次跳转到该页面执行以上scope == "snsapi_userinfo"
        # 的逻辑，从而保存其信息
        check_openid = UserProfile.objects.filter(openid=fan_info['openid']).first()
        if not check_openid:
            # return render(request, 'register.html', {'url': web_get_code+'snsapi_userinfo#wechat_redirect','header':'认证提示','text':'你还未进行信息认证,请进行第一次认证'})
            return HttpResponseRedirect(web_get_code + 'snsapi_userinfo#wechat_redirect')
        #当非第一次登陆时，检测用户头像是否发生变化，若变化，则修改头像url。
        check_headimgurl = UserProfile.objects.filter(headimgurl = fan_info['headimgurl'], openid = fan_info['openid']).first()
        if not check_headimgurl:
            UserProfile.objects.filter(openid = fan_info['openid']).update(headimgurl = fan_info['headimgurl'])
        # response = HttpResponseRedirect('/index/')
        # response.set_cookie('fanid',check_openid.id,3600)
        # return response
        response = render_to_response('index.html', {'nickname': fan_info['nickname'], 'sex': fan_info['sex'], 'city': fan_info['city'], 'headimgurl': fan_info['headimgurl']})
        response.set_cookie('fanid', 'check_openid.id', 3600)
        return response

    def getindex(self, request):
        return render(request, 'index.html')

