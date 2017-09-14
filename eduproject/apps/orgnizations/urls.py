from django.conf.urls import url

from .views import OrgList, UserAsk, OrgHome, OrgCourses, OrgDesc, OrgTeacher, UserFavor, TeacherList, TeacherDetail

urlpatterns = [
    url(r'^list/$', OrgList.as_view(), name='orglist'),
    url(r'^userask/$', UserAsk.as_view(), name='userask'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHome.as_view(), name='orghome'),
    url(r'^courses/(?P<org_id>\d+)/$', OrgCourses.as_view(), name='courses'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDesc.as_view(), name='desc'),
    url(r'^org_teachers/(?P<org_id>\d+)/$', OrgTeacher.as_view(), name='teachers'),

    url(r'^favorite/$', UserFavor.as_view(), name='userfav'),

    url(r'^teacher/list/$', TeacherList.as_view(), name='teacher_list'),
    url(r'^teacher/detail/(?P<teacher_id>\d+)/$', TeacherDetail.as_view(), name='teacher_detail')
]
