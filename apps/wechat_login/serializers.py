# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2018/11/26 15:01'


from .models import DeclareProfile,UserProfile
from rest_framework import serializers

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeclareProfile
        fields = ('declareid', 'sender', 'towho', 'anonymous', 'imgurl', 'content', 'create_time')


class UsermessageSerrializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('nickname', 'sex', 'city', 'headimgurl', 'regist_time')

