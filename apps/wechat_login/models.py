# coding=utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.


class UserProfile(models.Model):
    openid = models.CharField(max_length=50, verbose_name='openid', default=u"", blank=True, null=True)
    nickname = models.CharField(max_length=50, verbose_name=u"昵称", default=u"", blank=True, null=True)
    sex = models.CharField(choices=(("1", u"男"),("2", '女'),("0", '未知')), default="0", max_length=8, blank=True, null=True)
    city = models.CharField(max_length=100, default=u"", blank=True, null=True)
    headimgurl = models.CharField(max_length=500, blank=True, null=True)
    major = models.CharField(max_length=100, default=u"", blank=True, null=True)

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.nickname

    # def create_user(user_message):




