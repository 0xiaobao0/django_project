# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-19 21:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='declareprofile',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u63d0\u4ea4\u65f6\u95f4'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='regist_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='\u6ce8\u518c\u65f6\u95f4'),
        ),
    ]
