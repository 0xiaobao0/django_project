# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2018/12/6 17:54'


from django.utils.deprecation import MiddlewareMixin

class Cors(MiddlewareMixin):
    def process_response(self, request, response):
        response['Access-Control-Allow-Origin'] = "*"
        return response