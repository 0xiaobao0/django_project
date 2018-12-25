# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2018/11/28 9:29'
from django import forms
from .models import DeclareProfile
from .models import UserProfile


class DeclareForm(forms.Form):
    sender = forms.IntegerField(required=True)
    towho = forms.CharField(max_length=40 ,required=True, error_messages={'required': u'请输入表白对象'})
    anonymous = forms.IntegerField(max_value=1, required=True, error_messages={'required': u'请选择是否匿名'})
    content = forms.CharField(max_length=4000, required=True, error_messages={'required': u'内容不能为空', 'max_length': u'超出最大长度'})
    imgurl = forms.CharField(required=False)

class DeclareModelForm(forms.ModelForm):
    class Meta:
        model = DeclareProfile
        fields = '__all__'
        exclude = ['create_time']

# class ChangeForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         fields = ['nickname', 'headimgurl', 'city' ,'sex']
