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
from django.views.generic.base import RedirectView

from django_project.settings import MEDIA_ROOT
from django.views.static import serve




userbond = wechat_login.views.web_authorization()



urlpatterns = [
    url(r'^favicon.ico$',RedirectView.as_view(url=r'static/favicon.ico')),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^forms/$', getform, name='go_form'),
    url(r'^auth/$', userbond.get),
    url(r'^index/$', userbond.getindex),
    url(r'^test/$', userbond.test),
    url(r'^declare/$', userbond.declaration),
    url(r'^upload/$', userbond.post),
    url(r'^media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),

]
