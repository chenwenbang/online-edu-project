# -*- coding:utf-8 -*-
import json

from django.shortcuts import render, HttpResponse
from django.views.generic.base import View
from django.db.models import Q

from .models import CourseOrg, City, Teacher
from .forms import UserAskForm
from operations.models import UserFavorite, Course


from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


class OrgList(View):

    def post(self, request):
        pass

    def get(self, request):

        orgs = CourseOrg.objects.all()
        citys = City.objects.all()
        hot_orgs = orgs.order_by('-click_nums')[:3]

        search_kw = request.GET.get('keywords','')

        if search_kw:
            orgs = orgs.filter(Q(name__icontains=search_kw)|Q(desc__icontains=search_kw))

        selected_city_id = request.GET.get('city', '')

        selected_org_type = request.GET.get('ct', '')

        sort_type = request.GET.get('sort','')

        if selected_city_id:
            orgs = orgs.filter(city_id=int(selected_city_id))

        if selected_org_type:
            orgs = orgs.filter(catgory=selected_org_type)

        if sort_type == 'courses':
            orgs = orgs.order_by('-course_nums')
        elif sort_type == 'students':
            orgs = orgs.order_by('-student_nums')

        nums = orgs.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(orgs, 5, request=request)
        forgs = p.page(page)

        return render(request, 'org-list.html', {'orgs':forgs, 'nums': nums, 'citys': citys,
                                                 'city_id':selected_city_id, 'category': selected_org_type,
                                                 'hot_orgs': hot_orgs, 'sort_type': sort_type})

        # pagination by myself
        '''
        one_page_nums = 10
        real_page_num = nums//one_page_nums + 1
        page_num = int(request.GET.get('page','1'))
        if page_num > real_page_num or page_num < 1:
            return HttpResponse('404 NOT FOUND')
        else:
            orgs = orgs[(page_num-1)*one_page_nums:one_page_nums*page_num]
        
        return render(request, 'org-list.html', {'orgs': orgs, 'citys': citys, 'real_page_num': xrange(1, real_page_num+1)})
        '''


class UserAsk(View):
    def post(self, request):
        ask_form = UserAskForm(request.POST)
        if ask_form.is_valid():
            user_ask = ask_form.save(commit=True)
            return HttpResponse(json.dumps({'status':'success'}))
        else:
            return HttpResponse(json.dumps({'status':'failed', 'msg':ask_form.errors}))

class UserFavor(View):
    def post(self, request):
        fav_id = request.POST.get('fav_id','0')
        fav_type = request.POST.get('fav_type','0')

        if request.user.is_authenticated():
            exist_record = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
            if exist_record:
                # 取消收藏
                exist_record.delete()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums -= 1
                    course.fav_nums = 0 if course.fav_nums < 0 else course.fav_nums
                    course.save()
                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums -= 1
                    org.fav_nums = 0 if org.fav_nums < 0 else org.fav_nums
                    org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums -= 1
                    teacher.fav_nums = 0 if teacher.fav_nums < 0 else teacher.fav_nums
                    teacher.save()
                return HttpResponse(json.dumps({'status':'success', 'msg':u'收藏'}))
            else:
                # 添加收藏
                if int(fav_type) > 0 and int(fav_id) > 0:
                    user_fav = UserFavorite()
                    user_fav.user = request.user
                    user_fav.fav_id = int(fav_id)
                    user_fav.fav_type = int(fav_type)
                    user_fav.save()

                    if int(fav_type) == 1:
                        course = Course.objects.get(id=int(fav_id))
                        course.fav_nums += 1
                        course.save()
                    elif int(fav_type) == 2:
                        org = CourseOrg.objects.get(id=int(fav_id))
                        org.fav_nums += 1
                        org.save()
                    elif int(fav_type) == 3:
                        teacher = Teacher.objects.get(id=int(fav_id))
                        teacher.fav_nums += 1
                        teacher.save()

                    return HttpResponse(json.dumps({'status':'success', 'msg':u'已收藏'}))
                else:
                    return HttpResponse(json.dumps({'status':'failed', 'msg':u'收藏出错啦'}))

        else:
            return HttpResponse(json.dumps({'status':'failed', 'msg':u'用户未登录'}))


class OrgHome(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))
        org.click_nums += 1
        org.save()
        courses = org.course_set.all()[:3]
        teacher = org.teacher_set.all()[:1]
        has_favor = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=org.id):
                has_favor = True
        return render(request, 'org-detail-homepage.html', {'courses':courses, 'teacher': teacher, 'org': org, 'current_page':'home', 'has_favor':has_favor})


class OrgCourses(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))
        courses = org.course_set.all()
        has_favor = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=org.id):
                has_favor = True
        return render(request, 'org-detail-course.html', {'courses': courses, 'org': org, 'current_page': 'courses', 'has_favor':has_favor})


class OrgDesc(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))
        has_favor = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=org.id):
                has_favor = True
        return render(request, 'org-detail-desc.html', {'org': org, 'current_page':'desc', 'has_favor':has_favor})


class OrgTeacher(View):
    def get(self, request, org_id):
        org = CourseOrg.objects.get(id=int(org_id))
        teachers = org.teacher_set.all()
        has_favor = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=org.id):
                has_favor = True
        return render(request, 'org-detail-teachers.html', {'org': org, 'teachers': teachers, 'current_page':'teachers', 'has_favor':has_favor})


class TeacherList(View):
    def get(self, request):
        teachers = Teacher.objects.all()
        sort = request.GET.get('sort','')
        sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:5]
        search_kw = request.GET.get('keywords', '')

        if search_kw:
            teachers = teachers.filter(Q(name__icontains=search_kw) | Q(org__name__icontains=search_kw))
        if sort:
            teachers = teachers.order_by('-click_nums')

        nums = teachers.count()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(teachers, 10, request=request)

        teachers = p.page(page)

        return render(request, 'teachers-list.html', {'teachers': teachers, 'sort': sort,
                                                      'nums': nums, 'sorted_teachers': sorted_teachers})


class TeacherDetail(View):

    def get(self, request, teacher_id):
        try:
            teacher = Teacher.objects.get(id=int(teacher_id))
        except Exception:
            return HttpResponse('404 NOT FOUND')
        else:
            teacher.click_nums += 1
            teacher.save()
            teacher_courses = teacher.course_set.all()
            sorted_teachers = Teacher.objects.all().order_by('-click_nums')[:5]
            has_fav_teacher = False
            has_fav_org = False
            if request.user.is_authenticated():
                if UserFavorite.objects.filter(user=request.user, fav_type=3, fav_id=teacher.id):
                    has_fav_teacher = True
                if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=teacher.org.id):
                    has_fav_org = True

            return render(request, 'teacher-detail.html', {
                'teacher': teacher,
                'teacher_courses': teacher_courses,
                'sorted_teachers': sorted_teachers,
                'has_fav_teacher': has_fav_teacher,
                'has_fav_org': has_fav_org
            })