# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from users.models import UserInfo
from courses.models import Course
# Create your models here.


class UserAsk(models.Model):
    name = models.CharField(max_length=20, verbose_name=u'姓名')
    phone = models.CharField(max_length=11, verbose_name=u'手机号')
    course_name = models.CharField(max_length=30, verbose_name=u'课程名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'客户咨询'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseComment(models.Model):
    user = models.ForeignKey(UserInfo, verbose_name=u'用户')
    course = models.ForeignKey(Course, verbose_name=u'课程')
    content = models.CharField(max_length=500, verbose_name=u'评论内容')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'评论时间')

    class Meta:
        verbose_name = u'评论'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.user, self.course)


class UserFavorite(models.Model):
    user = models.ForeignKey(UserInfo, verbose_name=u'用户')
    fav_type = models.IntegerField(default=1, choices=((1, '课程'), (2, '课程机构'), (3, '授课老师')),
                                   verbose_name=u'收藏类型')
    fav_id = models.IntegerField(default=0, verbose_name=u'收藏内容ID')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name


class UserMessage(models.Model):
    user = models.IntegerField(default=0, verbose_name=u'接收用户')  # 0表示广播，否则就填用户id
    message = models.CharField(max_length=500, verbose_name=u'消息内容')
    has_read = models.BooleanField(default=False, verbose_name=u'是否已读')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加信息')

    class Meta:
        verbose_name = u'用户消息'
        verbose_name_plural = verbose_name


class UserCourse(models.Model):
    user = models.ForeignKey(UserInfo, verbose_name=u'用户')
    course = models.ForeignKey(Course, verbose_name=u'所学课程')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'用户课程'
        verbose_name_plural = verbose_name