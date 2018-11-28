# coding=utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class UserProfile(models.Model):
    userid = models.AutoField(verbose_name=u'用户id', primary_key=True)
    openid = models.CharField(max_length=50, verbose_name='openid', default=None)
    nickname = models.CharField(max_length=50, verbose_name=u"昵称", default=u"", blank=True, null=True)
    sex = models.IntegerField(choices=((1, u"男"),(2, u'女'),(0, u'未知')), default="0", blank=True, null=True)
    city = models.CharField(max_length=100, default=u"", blank=True, null=True)
    headimgurl = models.CharField(max_length=500, blank=True, null=True)
    major = models.CharField(max_length=100, default=u"", blank=True, null=True)
    regist_time = models.DateTimeField(verbose_name=u'注册时间', auto_now_add=True)

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.nickname

    # def create_user(user_message):

class DeclareProfile(models.Model):
    declareid = models.AutoField(verbose_name=u'表白内容id', primary_key=True)
    sender = models.ForeignKey(UserProfile, verbose_name=u'发送者', default=u"", blank=True, null=True)
    towho = models.CharField(max_length=20, verbose_name=u'接受者', default=u"", blank=True, null=True)
    anonymous = models.IntegerField(verbose_name=u'是否匿名', choices=((1, u"匿名"), (0, "不匿名")), default=0, blank=True, null=True)
    imgurl= models.CharField(max_length=100, verbose_name=u'图片url', default=u"", blank=True, null=True)
    content = models.CharField(max_length=5000, verbose_name=u'内容', default=u"", blank=True, null=True)
    create_time = models.DateTimeField(verbose_name=u'提交时间', auto_now_add=True)

    class Meta:
        verbose_name = u"表白信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.sender.nickname




