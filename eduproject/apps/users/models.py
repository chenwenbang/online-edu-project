# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserInfo(AbstractUser):
    nickname = models.CharField(max_length=30, default='', verbose_name=u'昵称')
    birthday = models.DateField(null=True, blank=True, verbose_name=u'生日')
    gender = models.CharField(max_length=6, choices=(('male', u'男'), ('female', u'女')),
                              default=u'男', verbose_name=u'性别')
    address = models.CharField(max_length=100, default='', verbose_name=u'地址')
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name=u'手机号')
    head_img = models.ImageField(upload_to='image/%Y/%m', default='image/default.png',
                                 max_length=100, verbose_name=u'头像')

    def __unicode__(self):
        return self.username

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name


    def unread_counts(self):
        from operations.models import UserMessage
        return UserMessage.objects.filter(user=self.id, has_read=False).count()


class EmailVerify(models.Model):
    code = models.CharField(max_length=20, verbose_name=u'验证码')
    email = models.EmailField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(max_length=10, choices=(('register', u'注册'), ('forget', u'忘记密码'), ('rebind', u'绑定新邮箱')),
                                 verbose_name=u'验证码类型')
    send_date = models.DateTimeField(default=datetime.now, verbose_name=u'生成时间')

    def __unicode__(self):
        return '%s(%s)' % (self.code, self.email)

    class Meta:
            verbose_name = u'邮箱验证'
            verbose_name_plural = verbose_name


class BannerInfo(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(upload_to='banner/%Y/%m', verbose_name=u'轮播图', max_length=100)
    url = models.URLField(max_length=200, verbose_name=u'链接地址')
    index = models.IntegerField(default=100, verbose_name=u'显示顺序')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name
