# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from orgnizations.models import CourseOrg, Teacher


# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'课程名')
    descri = models.CharField(max_length=300, verbose_name=u'课程简介')
    detail = models.TextField(max_length=1000, verbose_name=u'课程详情')
    degree = models.CharField(max_length=10, choices=(('cj', '初级'), ('zj', '中级'), ('gj', '高级')),
                              verbose_name=u'课程难度')
    learn_time = models.IntegerField(default=0, verbose_name=u'课程时长')
    student_nums = models.IntegerField(default=0, verbose_name=u'学生人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m', verbose_name=u'封面图片', max_length=100)
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    category = models.CharField(max_length=20, verbose_name=u'课程类别', default=u'后端开发')
    tag = models.CharField(default='', verbose_name=u'课程标签', max_length=20)
    teacher = models.ForeignKey(Teacher, verbose_name=u'讲师', null=True, blank=True)
    you_need_know = models.CharField(max_length=300, verbose_name=u'课程须知', default='')
    teacher_tell_you = models.CharField(max_length=300, verbose_name=u'老师告诉你', default='')
    is_banner = models.BooleanField(default=False, verbose_name=u'是否轮播')


    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.name,self.org)

    def get_lesson_nums(self):
        return self.lesson_set.all().count()

    def get_learn_stus(self):
        return self.usercourse_set.all()[:5]

    def get_lesson(self):
        return self.lesson_set.all()

    def get_sources(self):
        return self.courseresource_set.all()


class Lesson(models.Model):
    course = models.ForeignKey('Course', verbose_name=u'所属课程')
    name = models.CharField(max_length=50, verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程章节'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.name, self.course.name)

    def get_videos(self):
        return self.video_set.all()


class Video(models.Model):
    lesson = models.ForeignKey('Lesson', verbose_name=u'所属章节')
    name = models.CharField(max_length=50, verbose_name=u'视频名')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    url = models.CharField(max_length=300, verbose_name=u'视频地址', default='')

    class Meta:
        verbose_name = u'课程视频'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey('Course', verbose_name=u'所属课程')
    name = models.CharField(max_length=100, verbose_name=u'课件名')
    download = models.FileField(upload_to='course/resource/%Y/%m', verbose_name=u'下载', max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.name