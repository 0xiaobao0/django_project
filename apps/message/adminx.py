# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2018/11/1 15:14'

import xadmin

# Register your models here.

from .models import UserMessage


class UserMessageAdmin(object):
    pass


xadmin.site.register(UserMessage, UserMessageAdmin)