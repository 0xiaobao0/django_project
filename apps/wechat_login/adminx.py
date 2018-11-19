# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2018/11/18 13:24'

import xadmin

# Register your models here.

from .models import DeclareProfile,UserProfile

class DeclareProfileAdmin(object):
    pass


class UserProfileAdmin(object):
    pass


xadmin.site.register(DeclareProfile, DeclareProfileAdmin)
xadmin.site.register(UserProfile, UserProfileAdmin)