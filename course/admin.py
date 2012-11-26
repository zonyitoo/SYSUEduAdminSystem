from django.contrib import admin
from course.models import *

admin.site.register(CourseMeta)
admin.site.register(CourseType)
admin.site.register(Course)
admin.site.register(CourseTime)
admin.site.register(CourseLocation)
