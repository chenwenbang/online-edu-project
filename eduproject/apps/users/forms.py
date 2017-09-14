# -*-coding:utf-8 -*-
from django import forms
from captcha.fields import CaptchaField
from .models import UserInfo

class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(min_length=8, max_length=20)
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ForgetPwdForm(forms.Form):
    email = forms.EmailField()
    captcha = CaptchaField(error_messages={'invalid': u'验证码错误'})


class ResetPwdForm(forms.Form):
    email = forms.EmailField()
    password1 = forms.CharField(min_length=8, required=True)
    password2 = forms.CharField(min_length=8, required=True)
    email_code = forms.CharField(required=True)


class UploadImageForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ['head_img']


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(min_length=8, max_length=20, required=True)
    password2 = forms.CharField(min_length=8, max_length=20, required=True)


class SendMailForm(forms.Form):
    email = forms.EmailField(required=True)


class RebindForm(forms.Form):
    email = forms.EmailField(required=True)
    email_code = forms.CharField(required=True)


class UserInfoForm(forms.ModelForm):

    class Meta:
        model = UserInfo
        fields = ['nickname', 'birthday', 'gender', 'address', 'phone']


