# -*- coding:utf-8 -*-

import json

from django.shortcuts import render, HttpResponse
from django.db.models import Q
from django.views.generic.base import View

from .models import Course
from operations.models import UserFavorite, CourseComment, UserCourse

from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from utils.mixin_utils import LoginRequiredMixin

# Create your views here.


class CourseList(View):
    def get(self, request):
        courses = Course.objects.all()
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        sort_type = request.GET.get('sort', '')
        search_kw = request.GET.get('keywords', '')

        if search_kw:
            courses = courses.filter(Q(name__icontains=search_kw)|Q(descri__icontains=search_kw)|Q(detail__icontains=search_kw))

        if sort_type == 'students':
            courses = courses.order_by('-student_nums')
        elif sort_type == 'hot':
            courses = courses.order_by('-click_nums')
        else:
            courses = courses.order_by('-add_time')

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(courses, 9, request=request)
        courses = p.page(page)
        return render(request, 'course-list.html', {'courses':courses, 'sort':sort_type,
                                                    'hot_courses':hot_courses})


class CourseDetail(View):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=int(course_id))
        except Exception:
            return HttpResponse(u'404 NOT FOUND')
        else:
            course.click_nums += 1
            course.save()
            has_fav_course = False
            has_fav_org = False
            if request.user.is_authenticated():
                if UserFavorite.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                    has_fav_course = True
                if UserFavorite.objects.filter(user=request.user, fav_id=course.org.id, fav_type=2):
                    has_fav_org = True

            tag = course.tag
            related_courses = []
            if tag:
                related_courses = Course.objects.filter(~Q(id=course_id),tag=tag)
            return render(request, 'course-detail.html', {'course': course, 'related_courses':related_courses,
                                                          'has_favor_course':has_fav_course,
                                                          'has_favor_org':has_fav_org})


class CourseInfo(LoginRequiredMixin, View):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=int(course_id))
        except Exception:
            return HttpResponse('404 NOT FOUND')
        else:

            #查询是否已经关联了该课程
            user_courses = UserCourse.objects.filter(user=request.user, course=course)
            if not user_courses:
                UserCourse.objects.create(user=request.user, course=course)
                course.student_nums += 1
                course.save()
                course.org.student_nums += 1
                course.org.save()

            user_courses = UserCourse.objects.filter(course=course)
            user_ids = [user_course.user.id for user_course in user_courses]
            all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)
            course_ids = [ucourse.course.id for ucourse in all_user_courses]
            related_courses = Course.objects.filter(~Q(id=int(course_id)), id__in=course_ids).order_by('-click_nums')[:5]
            return render(request, 'course-video.html', {'course': course, 'related_courses':related_courses})


class CourseComments(LoginRequiredMixin, View):
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id=int(course_id))
        except Exception:
            return HttpResponse('404 NOT FOUND')
        else:
            current_user_courses = UserCourse.objects.filter(course=course)
            user_ids = [user_course.user.id for user_course in current_user_courses]
            user_courses = UserCourse.objects.filter(user_id__in=user_ids)
            course_ids = [ucourse.course.id for ucourse in user_courses]
            related_courses = Course.objects.filter(~Q(id=int(course_id)), id__in=course_ids).order_by('-click_nums')[:5]
            comments = CourseComment.objects.filter(course=course)
            return render(request, 'course-comment.html', {'course': course,
                                                           'comments':comments,
                                                           'related_courses':related_courses})


class AddComment(View):
    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponse(json.dumps({'status':'failed', 'msg':u'用户未登录'}))

        course_id = request.POST.get('course_id', 0)
        comment = request.POST.get('comment', '')

        if course_id > 0 and comment:
            course_comment = CourseComment()
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.content = comment
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse(json.dumps({'status': 'success', 'msg': u'评论成功'}))
        else:
            return HttpResponse(json.dumps({'status': 'failed', 'msg': u'评论失败'}))
