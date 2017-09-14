import xadmin

from .models import Course, Lesson, Video, CourseResource


class CourseAdmin(object):
    list_display = ['name', 'degree', 'org', 'descri']
    search_fields = ['name', 'degree', 'org', 'descri']
    list_filter = ['name', 'degree', 'org', 'descri']

class LessonAdmin(object):
    list_display = ['name', 'course']
    search_fields = ['name', 'course']
    list_filter = ['name', 'course']


class VideoAdmin(object):
    list_display = ['name', 'lesson', 'url']
    search_fields = ['name', 'lesson', 'url']
    list_filter = ['name', 'lesson', 'url']


class CourseResourceAdmin(object):
    list_display = ['name', 'course', 'download']
    search_fields = ['name', 'course', 'download']
    list_filter = ['name', 'course', 'download']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)