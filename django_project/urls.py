"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from message.views import getform
import wechat_login.views
from django.contrib import admin
import xadmin

userbond = wechat_login.views.web_authorization()



urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^forms/$', getform, name='go_form'),
    url(r'^auth/$', userbond.get)
]
