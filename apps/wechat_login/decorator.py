# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2018/11/27 16:50'


from django.http import HttpResponse
from django.shortcuts import render
import json


# def check_login(func):
#     def wrapper(self, request):
#         islogin = request.session.get('islogin')
#         if (islogin == True):
#             return func(self, request)
#         else:
#             data = {}
#             data['status'] = 4001
#             data['message'] = u'no login'
#             return HttpResponse(json.dumps(data), content_type="application/json")
#     return wrapper


def check_login(func):
    def wrapper(self, request):
        islogin = request.session.get('islogin')
        if (islogin == True):
            return func(self, request)
        else:
            data = {}
            data['status'] = 4001
            data['message'] = u'no login'
            return HttpResponse(json.dumps(data), content_type="application/json")
    return wrapper


