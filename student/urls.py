from django.conf.urls import patterns, include, url

urlpatterns = patterns('', 
    url('selectCourses/$', 'student.views.select_courses'),
    url('redrawalCourses/$', 'student.views.redrawal_courses'),
)
