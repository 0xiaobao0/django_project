# coding=utf-8
__author__ = 'wangchuan'
__date__ = '2018/11/9 13:47'

app_id = 'wxb0b4327e8a283ae6'
app_secret = '0259f25925f82e5415085b0c8e0c397e'
redirect_url = '0smallwhite0.vicp.io:16991/'
state = 'STATE'

web_get_code = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid=%s&redirect_uri=%s&response_type=code&state=%s&scope='%(app_id,redirect_url,state)
web_get_fan_info = 'https://api.weixin.qq.com/sns/userinfo?access_token='
web_check_access_token = 'https://api.weixin.qq.com/sns/auth?access_token='
web_get_access_token = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid=%s&secret=%s&grant_type=authorization_code&code='%(app_id,app_secret)
