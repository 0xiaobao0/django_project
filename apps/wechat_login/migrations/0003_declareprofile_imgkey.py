# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-11-21 17:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wechat_login', '0002_auto_20181119_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='declareprofile',
            name='imgkey',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
