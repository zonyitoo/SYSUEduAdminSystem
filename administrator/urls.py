from django.conf.urls import patterns, include, url

urlpatterns = patterns('', 
    #url('selectCourse/$', 'student.views.select_course'),
    #url('withdrawalCourse/$', 'student.views.withdrawal_course'),
    url('getStudentSheet/(.*.xls)$', 'administrator.views.get_student_sheet'),
)
