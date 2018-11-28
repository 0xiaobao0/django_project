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
from wechat_login.views import *
from django.contrib import admin
import xadmin
from django.views.generic.base import RedirectView

from django_project.settings import MEDIA_ROOT
from django.views.static import serve

from django.conf.urls import url, include
from rest_framework import routers



urlpatterns = [
    url(r'^favicon.ico$',RedirectView.as_view(url=r'static/favicon.ico')),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^forms/$', getform, name='go_form'),
    url(r'^auth/$', Web_authorization.as_view()),
    url(r'^index/$', UsermessageViewSet.as_view()),
    url(r'^test/$', test),
    url(r'^declare/$', Declaration.as_view()),
    # url(r'^upload/$', Upload.as_view(), name='upload'),
    # url(r'^upload_status/$', userbond.upload_status),
    url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),
    # url(r'^show/$', show_messages),
    url(r'^messages/$', MessageViewSet.as_view(), name='message_list'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))

]
