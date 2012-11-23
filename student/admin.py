from django.contrib import admin
from student.models import *

admin.site.register(Student)
admin.site.register(StudentMeta)
admin.site.register(StudentMinor)

