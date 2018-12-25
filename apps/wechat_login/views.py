# coding=utf-8
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect, render_to_response
from django.core import serializers
from django.template import RequestContext
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from .models import UserProfile
from .models import DeclareProfile
import requests
import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination, CursorPagination
from .serializers import MessageSerializer, UsermessageSerrializer

from .decorator import check_login

from .forms import DeclareModelForm, DeclareForm

from django.forms.models import model_to_dict


# Create your views here.
class Message_Page(LimitOffsetPagination):
    default_limit = 12  # 一页默认几个
    limit_query_param = 'limit'  # 关键字后面跟的是一页显示几个
    offset_query_param = 'offset'  # 这个后面跟的是从哪里显示
    max_limit = 24  # 这个是一页最多显示有几个


# 如果把数据放在对象里面，就要变成字典形式即可


class BaseResponse(object):
    def __init__(self, result=None, code=1000, message=None, data=None, error=None):
        self.result = {}
        self.result['code'] = code
        self.result['message'] = message
        self.result['data'] = data
        self.result['error'] = error


class Web_authorization(View):
    def get(self, request):
        ret = BaseResponse()
        from wechatconfig import web_get_code, web_get_fan_info, web_get_access_token, web_check_access_token
        code = request.GET.get("code", "")
        if not code:
            ret.result['code'] = 4004
            ret.result['error'] = 'Unauthorized user'
            return HttpResponse(json.dumps(ret.result), content_type="application/json")
        requests_web_get_access_token_result = requests.get(web_get_access_token + code).json()
        if 'errmsg' in requests_web_get_access_token_result.keys():
            print  requests_web_get_access_token_result['errmsg']
            return HttpResponseRedirect(web_get_code + 'snsapi_base#wechat_redirect')
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

class Change_usermessage(APIView):
    @check_login
    def post(self, request):
        ret = BaseResponse()
        try:
            useropenid = request.session.get('user_openid')
            user = UserProfile.objects.filter(openid=useropenid).first()
            user.nickname = request.POST.get('nickname', user.nickname)
            user.sex = request.POST.get('sex', user.sex)
            user.headimgurl = request.POST.get('headimgurl', user.headimgurl)
            user.city = request.POST.get('city', user.city)
            user.save()
            ret.result['code'] = 2200
            ret.result['message'] = 'change message success'
            ret.result['data'] = {
                'nickname': user.nickname,
                'sex': user.sex,
                'headimgurl': user.headimgurl,
                'city': user.city
            }
        except:
            ret.result['code'] = 4200
            ret.result['message'] = 'change message faild'
        return Response(ret.result)







def test(request):
    request.session['user_openid'] = 'ozKcL0l3gjCmZrSGKLMMIFvT-9B8'  # 在Django 中一句话搞定
    request.session['islogin'] = True
    # request.session.flush()
    return redirect('/index')


class UsermessageViewSet(APIView):
    @check_login
    def get(self, request, format=None):
        ret = BaseResponse()
        try:
            useropenid = request.session.get('user_openid')
            user_message = UserProfile.objects.filter(openid=useropenid)  # 千万不要在后面加上.first()!!!!!!!!!!!!!
            serializer = UsermessageSerrializer(instance=user_message, many=True)
            ret.result['code'] = 2000
            ret.result['message'] = "Successful access to user information"
            ret.result['data'] = serializer.data
            return Response(ret.result)
        except:
            ret.result['code'] = 4002
            ret.result['error'] = "Can't found the user"
            return Response(ret.result)


class MessageViewSet(APIView):
    def get(self, request, format=None):
        ret = BaseResponse()
        try:
            messages = DeclareProfile.objects.all().order_by('-create_time')  # 找到所有的数据项
            message_Page = Message_Page()  # 实例化分页器，
            page_message_list = message_Page.paginate_queryset(queryset=messages, request=request,
                                                               view=self)  # 把数据放在分页器上面
            serializer = MessageSerializer(instance=page_message_list, many=True)  # 序列化数据
            ret.result['code'] = 2001
            ret.result['message'] = 'Successful Access to Presentation Information'
            ret.result['data'] = serializer.data
            ret.next = message_Page.get_next_link()
        except Exception as e:
            ret.result['code'] = 4003
            ret.result['error'] = u'Faild to get Presentation Information'
        return Response(ret.result)

        # def post(self, request, format=None):
        #     serializer = MessageSerializer(data=request.data)
        #     if serializer.is_valid():
        #         serializer.save()
        #         return Response(serializer.data, status=status.HTTP_201_CREATED)
        #     else:
        #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #         # return  p1.get_paginated_response(ret)#这个会显示上一页和下一页
        #         # return  p1.get_paginated_response(ser.data)


def get_qiniu_token_and_key(request):
    import qiniu
    import uuid
    ACCESS_KEY = 'EI5u9AjeOC8Z6E-dO8779gUHFvn2OzZygG6TTaWy'
    SECRET_KEY = 'UhfftOyhvZ4rYYrxVkwkg-KD0Xtf685zTkYZAXz9'
    BUCKET_NAME = '0store0'
    key = str(uuid.uuid1()).replace('-', '')  # 这里使用uuid作为保存在七牛里文件的名字。并去掉了uuid中的“-”
    q = qiniu.Auth(ACCESS_KEY, SECRET_KEY)
    token = q.upload_token(BUCKET_NAME, key, 7200, {
        'returnBody': '{"name": "$(fname)", "key": "$(key)"}',
        'fsizeLimit': 5242880,
        'mimeLimit': 'image/*'
    })
    data = {'token': token, 'key': key}
    return HttpResponse(json.dumps(data), content_type="application/json")


class Declaration(APIView):
    def get(self, request):
        import qiniu
        import uuid
        ACCESS_KEY = 'EI5u9AjeOC8Z6E-dO8779gUHFvn2OzZygG6TTaWy'
        SECRET_KEY = 'UhfftOyhvZ4rYYrxVkwkg-KD0Xtf685zTkYZAXz9'
        BUCKET_NAME = '0store0'
        key = str(uuid.uuid1()).replace('-', '')  # 这里使用uuid作为保存在七牛里文件的名字。并去掉了uuid中的“-”
        q = qiniu.Auth(ACCESS_KEY, SECRET_KEY)
        token = q.upload_token(BUCKET_NAME, key, 7200, {
            'returnBody': '{"name": "$(fname)", "key": "$(key)"}',
            'fsizeLimit': 5242880,
            'mimeLimit': 'image/*'
        })
        data = {'token': token, 'key': key}
        token_key_dict = data
        return render(request, 'upload.html', token_key_dict)

    # @check_login
    def post(self, request):
        ret = BaseResponse()
        if True:
            form_querydict = request.POST
            new_form_querydict = form_querydict.copy()
            useropenid = request.session.get('user_openid')
            userid = UserProfile.objects.filter(openid=useropenid).first().userid
            new_form_querydict.__setitem__('sender', userid)
            declare_form = DeclareForm(new_form_querydict)
            declare_model_form = DeclareModelForm(new_form_querydict)
            valid = declare_form.is_valid()
            if valid == True:
                declare_model_form.save()
                ret.result['code'] = 2002
                ret.result['message'] = 'save succeed'
                ret.result['data'] = {'imgurl': new_form_querydict.get('imgurl')}
            else:
                result_dict = get_qiniu_token_and_key(request)
                result_dict['form'] = declare_form
                return render(request, 'upload.html', result_dict)
        else:
            ret.result['code'] = 4004
            ret.result['error'] = 'Faild to upload'
        return Response(ret.result)
