# coding=utf-8
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class UserMessage(models.Model):
    name = models.CharField(max_length=20, null=True, blank=True, default="", verbose_name=u"姓名")
    email = models.EmailField(verbose_name=u"邮箱")
    address = models.CharField(max_length=50, verbose_name=u"地址")
    message = models.CharField(max_length=1000, verbose_name=u"留言")

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name


