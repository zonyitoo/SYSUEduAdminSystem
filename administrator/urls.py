from django.conf.urls import patterns, include, url

urlpatterns = patterns('', 
    #url('selectCourse/$', 'student.views.select_course'),
    #url('withdrawalCourse/$', 'student.views.withdrawal_course'),
    url('getStudentSheet/(.*.xls)$', 'administrator.views.get_student_sheet'),
    url('uploadStudentSheet/$', 'administrator.views.upload_student_sheet'),
    url('getTeacherSheet/(.*.xls)$', 'administrator.views.get_teacher_sheet'),
    url('uploadTeacherSheet/$', 'administrator.views.upload_teacher_sheet'),

    ## Select Course
    url('getSelectCourseState/$',
        'administrator.views.get_select_course_state'),
    url('openSelectCourse/$', 'administrator.views.open_select_course'),
    url('closeSelectCourse/$', 'administrator.views.close_select_course'),

    ## Course screen
    url('toggleCourseScreen/$', 'administrator.views.toggle_course_screen'),
    url('getScreenState/$', 'administrator.views.get_course_screen_state'),

    ## Upload score
    url('openUploadScore/$', 'administrator.views.open_upload_score'),
    url('closeUploadScore/$', 'administrator.views.close_upload_score'),
    url('getUploadScoreState/$', 'administrator.views.get_upload_score_state'),
)
