from django.conf.urls import url

from .views import CourseList, CourseDetail, CourseInfo, CourseComments, AddComment

urlpatterns = [
    url('^list/$', CourseList.as_view(), name='courselist'),
    url('^detail/(?P<course_id>\d+)/$', CourseDetail.as_view(), name='coursedetail'),
    url('^info/(?P<course_id>\d+)/$', CourseInfo.as_view(), name='courseinfo'),
    url('^comment/(?P<course_id>\d+)/$', CourseComments.as_view(), name='coursecomment'),
    url('^add_comment/$', AddComment.as_view(), name='addcomment')
]