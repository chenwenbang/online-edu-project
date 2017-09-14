from django.conf.urls import url

from .views import UserInfomation, UserImageUpload, ModifyPwd, \
                    SendMailView, Rebind, MyCourses, MyFavOrg, \
                    MyFavTeacher, MyFavCourse, MyMessage

urlpatterns = [
    url(r'^info/$', UserInfomation.as_view(), name='info'),
    url(r'^image/upload/$', UserImageUpload.as_view(), name='image_upload'),
    url(r'^modify_pwd/$', ModifyPwd.as_view(), name='modify_pwd'),
    url(r'^sendmail/$', SendMailView.as_view(), name='sendmail'),
    url(r'^rebind/$', Rebind.as_view(), name='rebind'),
    url(r'^mycourses/$', MyCourses.as_view(), name='mycourses'),
    url(r'^myfav/org/$', MyFavOrg.as_view(), name='myfav_org'),
    url(r'^myfav/teacher/$', MyFavTeacher.as_view(), name='myfav_teacher'),
    url(r'^myfav/course/$', MyFavCourse.as_view(), name='myfav_course'),
    url(r'^mymessage/$', MyMessage.as_view(), name='my_message')
]