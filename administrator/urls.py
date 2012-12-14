from django.conf.urls import patterns, include, url

urlpatterns = patterns('', 
    #url('selectCourse/$', 'student.views.select_course'),
    #url('withdrawalCourse/$', 'student.views.withdrawal_course'),
    url('getStudentSheet/(.*.xls)$', 'administrator.views.get_student_sheet'),
    url('uploadStudentSheet/$', 'administrator.views.upload_student_sheet'),
    url('getTeacherSheet/(.*.xls)$', 'administrator.views.get_teacher_sheet'),
    url('uploadTeacherSheet/$', 'administrator.views.upload_teacher_sheet'),
    url('toggleSelectCourse/$', 'administrator.views.toggle_select_course'),
    url('toggleCourseScreen/$', 'administrator.views.toggle_course_screen'),
    url('toggleUploadScore/$', 'administrator.views.toggle_upload_score'),
)
