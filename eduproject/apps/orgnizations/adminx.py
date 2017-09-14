import xadmin

from .models import CourseOrg, City, Teacher


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'city', 'catgory', 'get_course_nums']
    search_fields = ['name', 'desc', 'city', 'catgory']
    list_filter = ['name', 'desc', 'city', 'catgory']


class CityAdmin(object):
    pass


class TeacherAdmin(object):
    list_display = ['name', 'org', 'work_years', 'work_company', 'work_position']
    search_fields = ['name', 'org', 'work_years', 'work_company', 'work_position']
    list_filter = ['name', 'org', 'work_years', 'work_company', 'work_position']

xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(City, CityAdmin)
xadmin.site.register(Teacher, TeacherAdmin)