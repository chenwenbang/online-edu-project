# -*- coding: utf-8 -*-

"""eduproject URL Configuration

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
from django.conf.urls import url, include

from django.views.static import serve

import xadmin
from settings import MEDIA_ROOT
from users.views import UserLogin, Register, Active, ForgetPwd, ResetPwd, UserLogout, IndexView



urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', UserLogin.as_view(), name='login'),
    url(r'^register/$', Register.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active(?P<active_code>\d+)/$', Active.as_view()),
    url(r'^forgetpwd/$', ForgetPwd.as_view(), name='forgetpwd'),
    url(r'^resetpwd/$', ResetPwd.as_view(), name='resetpwd'),
    url(r'^logout/$', UserLogout.as_view(), name='logout'),

    #org
    url(r'^org/', include('orgnizations.urls', namespace='org')),

    #course
    url(r'^course/', include('courses.urls', namespace='course')),

    #user
    url(r'^user/', include('users.urls', namespace='user')),

    #media
    url(r'media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
]

#404
handler404 = 'users.views.page_not_found'

#500
handler500 = 'users.views.page_error'