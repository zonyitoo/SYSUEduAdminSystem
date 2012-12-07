from django.conf.urls import patterns, include, url

urlpatterns = patterns('', 
    #url('selectCourse/$', 'student.views.select_course'),
    #url('withdrawalCourse/$', 'student.views.withdrawal_course'),
    url('getStudentSheet/(.*.xls)$', 'administrator.views.get_student_sheet'),
    url('uploadStudentSheet/$', 'administrator.views.upload_student_sheet'),
    url('getStudentList/$', 'administrator.views.get_student_list'),
    url('getTeacherList/$', 'administrator.views.get_teacher_list'),
    url('getTeacherSheet/(.*.xls)$', 'administrator.views.get_teacher_sheet'),
    url('uploadTeacherSheet/$', 'administrator.views.upload_teacher_sheet'),
)
