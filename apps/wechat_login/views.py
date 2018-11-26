# coding=utf-8
from django.views.generic import View
from django.http import HttpResponseRedirect
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import render, redirect, render_to_response
from django.template import RequestContext
from django.core.cache import cache
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
from .models import DeclareProfile
import requests
import json

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination,PageNumberPagination,CursorPagination
from .serializers import MessageSerializer
# import time
#
# from qiniu import Auth, put_file, etag
# import qiniu.config
#
# accessKey  = 'EI5u9AjeOC8Z6E-dO8779gUHFvn2OzZygG6TTaWy'
# secretKey = 'UhfftOyhvZ4rYYrxVkwkg-KD0Xtf685zTkYZAXz9'
# bucket = '0store0'
# domain = 'img.hellowmrliu.cn'

# Create your views here.
class P1(LimitOffsetPagination):
    default_limit =1#一页默认几个
    limit_query_param = 'limit' #关键字后面跟的是一页显示几个
    offset_query_param = 'offset'#这个后面跟的是从哪里显示
    max_limit = 10 #这个是一页最多显示有几个
#如果把数据放在对象里面，就要变成字典形式即可


class BaseResponse(object):
    def __init__(self,code=1000,data=None,error=None):
        self.code=code
        self.data=data
        self.error=error


class MessageViewSet(APIView):
    def get(self, request, format=None):
        ret = BaseResponse()
        try:
            messages = DeclareProfile.objects.all()#找到所有的数据项
            p1 = P1()#实例化分页器，
            page_message_list = p1.paginate_queryset(queryset=messages, request=request, view=self)#把数据放在分页器上面
            serializer = MessageSerializer(instance=page_message_list, many=True)#序列化数据
            ret.data = serializer.data
            ret.next = p1.get_next_link()
        except Exception as e:
            ret.code = 1001
            ret.error = u'获取信息失败'
        return Response(ret.data)

    def post(self, request, format=None):
        serializer = MessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            # return  p1.get_paginated_response(ret)#这个会显示上一页和下一页
            # return  p1.get_paginated_response(ser.data)


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


    def test(self, request):
        request.session['user_openid'] = 'ozKcL0l3gjCmZrSGKLMMIFvT-9B8'  # 在Django 中一句话搞定
        request.session['islogin'] = True
        return redirect('/index')

    def jugelogin(self, request):
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
                profile = DeclareProfile()
                profile.sender_id = userid
                profile.towho=request.POST.get('towho', '')
                profile.anonymous=request.POST.get('anonymous', '')
                profile.content=request.POST.get('content', '')
                profile.imgurl = request.POST.get('img_url', '')
                profile.save()
            return HttpResponse(u'提交保存成功')


    def upload_img(self,request):
        import qiniu
        import uuid
        result = self.jugelogin(request)
        if 'errmsg' in result.keys():
            return HttpResponse(result['errmsg'])
        else:
            useropenid = result['openid']
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
        return render(request, 'upload.html', {'token': token, 'key': key})


    def show_messages(self,request):
        from django.core import serializers
        messages = DeclareProfile.objects.all()[:2]
        json_data = serializers.serialize('json', messages)
        json_data = json.loads(json_data)
        pass








