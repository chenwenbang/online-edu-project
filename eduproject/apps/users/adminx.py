# -*- coding:utf-8 -*-

import xadmin
from xadmin import views  # for whole site settings

from .models import EmailVerify, BannerInfo


class BaseSettings(object):  # the whole site settings
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):
    site_title = u'这是朕的江山呐！'
    site_footer = u'朕的江山'
    menu_style = 'accordion'


class EmailVerifyAdmin(object):

    list_display = ['code', 'email', 'send_type', 'send_date']
    search_fields = ['code', 'email', 'send_type']
    list_filter = ['code', 'email', 'send_type', 'send_date']




class BannerInfoAdmin(object):

    list_display = ['title', 'url', 'index']
    search_fields = ['title', 'url', 'index']
    list_filter = ['title', 'index']



xadmin.site.register(EmailVerify, EmailVerifyAdmin)
xadmin.site.register(BannerInfo, BannerInfoAdmin)

xadmin.site.register(views.BaseAdminView, BaseSettings)
xadmin.site.register(views.CommAdminView, GlobalSettings)

