from django.contrib import admin
from take.models import *

class TakesAdmin(admin.ModelAdmin):
    list_display = ('student', 'course')

admin.site.register(Takes, TakesAdmin)
