# -*- coding: utf-8 -*_

from random import Random
from django.core.mail import send_mail
from datetime import datetime

from users.models import EmailVerify
from eduproject.settings import EMAIL_FROM

def send_email(email, type='register'):
    code = random_code(6)

    email_title = ''
    email_body = ''

    if type == 'register':
        EmailVerify.objects.create(email=email, code=code, send_type=type)
        email_title = u'在线教育网注册激活链接'
        email_body = u'请点击下方链接激活你的账号：http://192.168.2.72:8000/active%s' %(code)

        status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if status:
            pass
    elif type == 'forget':
        ev = EmailVerify.objects.filter(email=email)
        if ev.count():
            ev.update(code=code, send_type=type, send_date=datetime.now())
        else:
            EmailVerify.objects.create(email=email, code=code, send_type=type)
        email_title = u'在线教育网重置密码'
        email_body = u'您的验证码为：%s' %(code)

        status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if status:
            pass
    elif type == 'rebind':
        EmailVerify.objects.create(email=email, code=code, send_type=type)
        email_title = u'在线教育网绑定新邮箱'
        email_body = u'您的验证码为：%s' % (code)

        status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if status:
            pass



def random_code(code_length):
    code = ''
    chars = '123456789'
    length = len(chars) - 1
    rd = Random()
    for _ in range(code_length):
        code += chars[rd.randint(0, length)]

    return code