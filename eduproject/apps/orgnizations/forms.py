# -*- coding:utf-8 -*-
from django import forms
from django.core.exceptions import ValidationError

from operations.models import UserAsk

import re

def mobile_validate(vaule):
    mobile_re = re.compile(r'^(13\d|15\d|17[678]|18\d|14[57])[0-9]{8}$')
    if not mobile_re.match(vaule):
        raise ValidationError(u'手机号格式不正确')

class UserAskForm(forms.ModelForm):
    # phone = forms.CharField(required=True, validators=[mobile_validate]) #覆盖model中的字段，优先级高

    class Meta:
        model = UserAsk
        fields = ['name', 'course_name', 'phone']  #这些是要存到数据库的字段

    # 另一种验证手机号的方法，修改了验证规则
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        mobile_re = re.compile(r'^(13\d|15\d|17[678]|18\d|14[57])[0-9]{8}$')
        if mobile_re.match(phone):
            return phone
        else:
            raise ValidationError(u'手机号有误', code='InvalidPhone')




