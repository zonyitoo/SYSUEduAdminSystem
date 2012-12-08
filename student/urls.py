from django.conf.urls import patterns, include, url

urlpatterns = patterns('', 
    #url('selectCourse/$', 'student.views.select_course'),
    #url('withdrawalCourse/$', 'student.views.withdrawal_course'),
    url('toggleCourse/$', 'student.views.toggle_course'),
    url('getStudentList/$', 'student.views.get_student_list'),
)
