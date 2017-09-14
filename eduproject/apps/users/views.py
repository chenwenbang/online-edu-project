# -*- coding:utf-8 -*-
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from django.contrib.auth.hashers import make_password
from django.core.urlresolvers import reverse

from .models import UserInfo, EmailVerify, BannerInfo
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ResetPwdForm, UploadImageForm,\
                   ModifyPwdForm, SendMailForm, RebindForm, UserInfoForm
from operations.models import UserCourse, UserFavorite, UserMessage
from courses.models import CourseOrg, Teacher, Course
from utils import email_sender
from utils.mixin_utils import LoginRequiredMixin
from pure_pagination import Paginator, PageNotAnInteger

import json
# Create your views here.


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserInfo.objects.get(Q(username=username)|Q(email=username))
            if user.check_password(password):
                return user
        except Exception:
            return None

class UserLogin(View):

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            uname = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(username=uname, password=pwd)  # 会将密码加密后验证，如果验证成功，则返回一个对象，否则返回None
            if user:
                if user.is_active:
                    login(request, user)
                    return redirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': u'账号未激活'})
            else:
                return render(request, 'login.html', {'msg':u'用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form':login_form})


class Register(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            if UserInfo.objects.filter(email=request.POST.get('email')):
                  # 邮箱已存在
                return render(request, 'register.html', {'register_form': register_form, 'msg': u'邮箱已存在'})
            else:
                new_user = UserInfo()
                new_user.username = request.POST.get('email')
                new_user.email = request.POST.get('email')
                new_user.is_active = False
                pwd = make_password(request.POST.get('password'))
                new_user.password = pwd
                new_user.save()

                # 增加一条欢迎注册消息
                msg = UserMessage()
                msg.user = new_user.id
                msg.message = u'{0},欢迎注册在线教育学习网！'.format(new_user.username)
                msg.save()

                email_sender.send_email(new_user.email, type='register')

                return redirect('/login/')

        else:
            return render(request, 'register.html', {'register_form': register_form})


class Active(View):
    def get(self, request, active_code):
        objs = EmailVerify.objects.filter(code=active_code)
        if objs:
            for obj in objs:
                UserInfo.objects.filter(email=obj.email).update(is_active=True)
            return redirect('/login/')
        else:
            return render(request, 'active_error.html')


class ForgetPwd(View):
    def get(self,request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forgetpwd_form':forgetpwd_form})

    def post(self, request):
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = forget_form.clean().get('email')
            if UserInfo.objects.filter(email=email):
                email_sender.send_email(email, 'forget')
                return render(request, 'password_reset.html', {'email': email})
            else:
                return render(request, 'forgetpwd.html', {'forgetpwd_form': forget_form, 'msg': u'用户不存在'})
        else:
            return render(request, 'forgetpwd.html', {'forgetpwd_form': forget_form})


class ResetPwd(View):
    def get(self, request):
        return redirect('/forgetpwd/')

    def post(self, request):
        resetpwd_form = ResetPwdForm(request.POST)
        if resetpwd_form.is_valid():
            email = resetpwd_form.clean().get('email')
            email_code = resetpwd_form.clean().get('email_code')
            pwd1 = resetpwd_form.clean().get('password1')
            pwd2 = resetpwd_form.clean().get('password2')
            ev = EmailVerify.objects.filter(email=email, code=email_code)
            if ev:
                if pwd1 == pwd2:
                    user = UserInfo.objects.filter(email=email).update(password=make_password(pwd1))
                    return render(request, 'password_reset.html', {'resetpwd_form': resetpwd_form, 'success': True})
                else:
                    return render(request, 'password_reset.html',
                                  {'resetpwd_form': resetpwd_form, 'password_msg': u'两次输入的密码不一致'})
            else:
                return render(request, 'password_reset.html', {'resetpwd_form': resetpwd_form, 'email_code_msg': u'验证码有误'})
        else:
            return render(request, 'password_reset.html', {'resetpwd_form': resetpwd_form})


class UserLogout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))


class UserInfomation(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'usercenter-info.html')

    def post(self, request):
        userinfo_form = UserInfoForm(request.POST, instance=request.user)
        if userinfo_form.is_valid():
            userinfo_form.save()
            return HttpResponse(json.dumps({'status':'success'}))
        else:
            return HttpResponse(json.dumps(userinfo_form.errors))



class UserImageUpload(LoginRequiredMixin, View):
    def post(self, request):
        # image_form = UploadImageForm(request.POST, request.FILES)
        # if image_form.is_valid():
        #     request.user.head_img = image_form.cleaned_data.get('head_img')
        #     request.user.save()
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse(json.dumps({'status':'success'}))
        else:
            return HttpResponse(json.dumps({'status': 'fail'}))


class ModifyPwd(View):
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = modify_form.cleaned_data.get('password1', '')
            pwd2 = modify_form.cleaned_data.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse(json.dumps({'status':'failed', 'msg':u'两次密码不一致'}))
            else:
                request.user.password = make_password(pwd1)
                request.user.save()
                return HttpResponse(json.dumps({'status':'success'}))
        else:
            return HttpResponse(json.dumps(modify_form.errors))


class SendMailView(LoginRequiredMixin, View):

    def get(self, request):
        mail_form = SendMailForm(request.GET)
        if mail_form.is_valid():
            new_email = mail_form.cleaned_data.get('email')
            if UserInfo.objects.filter(email=new_email):
                return HttpResponse(json.dumps({'email':u'邮箱已存在'}))
            else:
                email_sender.send_email(new_email, 'rebind')
                return HttpResponse(json.dumps({'status': 'success'}))


class Rebind(LoginRequiredMixin, View):

    def post(self, request):
        rebind_form = RebindForm(request.POST)
        if rebind_form.is_valid():
            new_email = rebind_form.cleaned_data.get('email')
            email_code = rebind_form.cleaned_data.get('email_code')
            ev = EmailVerify.objects.filter(email=new_email, code=email_code, send_type='rebind')
            if ev:
                request.user.email = new_email
                request.user.save()
                return HttpResponse(json.dumps({'status':'success'}))
            else:
                return HttpResponse(json.dumps({'email':u'验证码有误'}))
        else:
            return HttpResponse({'email':u'数据有误'})


class MyCourses(LoginRequiredMixin, View):
    def get(self, request):
        courses = UserCourse.objects.filter(user=request.user)
        return render(request, 'usercenter-mycourse.html', {'courses':courses})


class MyFavOrg(LoginRequiredMixin, View):
    def get(self, request):
        orgs = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)

        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            orgs.append(org)

        return render(request, 'usercenter-fav-org.html', {
            'orgs': orgs,
        })


class MyFavTeacher(LoginRequiredMixin, View):
    def get(self, request):
        teachers = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)

        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teachers.append(teacher)

        return render(request, 'usercenter-fav-teacher.html', {
            'teachers': teachers,
        })

class MyFavCourse(LoginRequiredMixin, View):
    def get(self, request):
        courses = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)

        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            courses.append(course)

        return render(request, 'usercenter-fav-course.html', {
            'courses': courses,
        })


class MyMessage(LoginRequiredMixin, View):
    def get(self, request):
        messages = UserMessage.objects.filter(user=request.user.id)

        unread_msgs = UserMessage.objects.filter(user=request.user.id, has_read=False)
        for unread_msg in unread_msgs:
            unread_msg.has_read = True
            unread_msg.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(messages, 5, request=request)

        messages = p.page(page)

        return render(request, 'usercenter-message.html', {'messages': messages})


class IndexView(View):
    def get(self, request):
        banners = BannerInfo.objects.all().order_by('index')
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        orgs = CourseOrg.objects.all()[:15]
        return render(request, 'index.html', {'banners':banners,
                                              'courses':courses,
                                              'banner_courses':banner_courses,
                                              'orgs':orgs})



def page_not_found(request):
    from django.shortcuts import render_to_response
    resp = render_to_response('404.html',{})
    resp.status_code = 404
    return resp

def page_error(request):
    from django.shortcuts import render_to_response
    resp = render_to_response('500.html',{})
    resp.status_code = 500
    return resp