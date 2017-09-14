# -*- coding:utf-8 -*-

from __future__ import unicode_literals
from datetime import datetime


from django.db import models

# Create your models here.


class CourseOrg(models.Model):
    name = models.CharField(max_length=30, verbose_name=u'机构名称')
    desc = models.TextField(verbose_name=u'机构描述')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    image = models.ImageField(upload_to='org/%Y%m', verbose_name=u'封面图')
    address = models.CharField(max_length=100, verbose_name=u'联系地址')
    city = models.ForeignKey('City', verbose_name='所在城市')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    catgory = models.CharField(default='school', max_length=20, choices=(('pxjg', u'培训机构'),('gr', u'个人'),('school', u'高校')), verbose_name=u'机构类别')
    student_nums = models.IntegerField(default=0, verbose_name=u'学习人数')
    course_nums = models.IntegerField(default=0, verbose_name=u'课程数')
    tag = models.CharField(default=u'知名高校', max_length=10)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'课程机构'
        verbose_name_plural = verbose_name

    def get_teacher_nums(self):
        return self.teacher_set.all().count()

    def get_course_nums(self):
        return self.course_set.all().count()

    get_course_nums.short_description = u'课程数'


class City(models.Model):
    name = models.CharField(max_length=10, verbose_name=u'城市名')
    desc = models.CharField(max_length=200, verbose_name=u'描述')
    add_time = models.DateTimeField(datetime.now)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    org = models.ForeignKey('CourseOrg', verbose_name=u'所属机构')
    name = models.CharField(max_length=20, verbose_name=u'教师名')
    work_years = models.IntegerField(default=0, verbose_name=u'工作年限')
    work_company = models.CharField(max_length=50, verbose_name=u'工作单位')
    work_position = models.CharField(max_length=50, verbose_name=u'工作职位')
    points = models.CharField(max_length=50, verbose_name=u'教学特点')
    click_nums = models.IntegerField(default=0, verbose_name=u'点击数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')
    image = models.ImageField(upload_to='teachers/%Y/%m', verbose_name=u'教师头像', max_length=100, default='')
    age = models.IntegerField(default=0, verbose_name=u'年龄')

    def __unicode__(self):
        return '{0}({1})'.format(self.name, self.org.name)

    class Meta:
        verbose_name = u'教师'
        verbose_name_plural = verbose_name

    def get_course_nums(self):
        return self.course_set.all().count()
