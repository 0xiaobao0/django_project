# coding=utf-8
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect
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
            return HttpResponseRedirect(web_get_code+'snsapi_base#wechat_redirect')
        if cache.has_key('web_access_token'):
            web_access_token = cache.get('web_access_token')
        else:
            web_access_token = requests_web_get_access_token_result['access_token']
            cache.set('web_access_token',web_access_token,110*60)
        fan_openid = requests_web_get_access_token_result['openid']
        # 这部分检验对于缓存来说是多余的，但是你如果担心缓存出问题，可以再次检验一波
        # check_access_token = requests.get(web_check_access_token+'%s&openid=%s'%(web_access_token,fan_openid)).json()
        # if check_access_token['errcode']!=0:
        #     return HttpResponseRedirect(web_get_code+'snsapi_base#wechat_redirect')
        scope = requests_web_get_access_token_result["scope"]
        if scope == "snsapi_userinfo":
            fan_info = requests.get(web_get_fan_info + '%s&openid=%s&lang=zh_CN' % (web_access_token, fan_openid))
            fan_info.encoding = 'utf-8'
            fan_info = fan_info.json()
            profile = UserProfile()
            profile.openid = fan_info['openid']
            profile.nickname = fan_info['nickname']
            profile.sex = fan_info['sex']
            profile.city = fan_info['city']
            profile.headimgurl = fan_info['headimgurl']
            profile.save()
        check_openid = UserProfile.objects.filter(openid=fan_openid).first()
        if not check_openid:
            return render(request, 'register.html', {'url': web_get_code+'snsapi_userinfo#wechat_redirect','header':'认证提示','text':'你还未进行信息认证,请进行第一次认证'})
        response = HttpResponseRedirect('/forms/')
        response.set_cookie('fanid',check_openid.id,3600)
        return response