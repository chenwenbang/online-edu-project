import xadmin
from .models import UserAsk, CourseComment, UserFavorite, UserCourse, UserMessage


class UserAskAdmin(object):
    list_display = ['name', 'phone', 'course_name', 'add_time']
    search_fields = ['name', 'phone', 'course_name']
    list_filter = ['name', 'phone', 'course_name', 'add_time']


class CourseCommentAdmin(object):
    list_display = ['user', 'course', 'content']
    search_fields = ['user', 'course', 'content']
    list_filter = ['user', 'course', 'content']


class UserFavoriteAdmin(object):
    list_display = ['user', 'fav_type', 'fav_id']
    search_fields = ['user', 'fav_type', 'fav_id']
    list_filter = ['user', 'fav_type', 'fav_id']


class UserCourseAdmin(object):
    list_display = ['user', 'course']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course']


class UserMessageAdmin(object):
    list_display = ['user', 'message', 'has_read']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComment, CourseCommentAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)