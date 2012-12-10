from django.conf.urls import patterns, url

urlpatterns = patterns('', 
    url('submitCourseAssessments/$',
        'assessment.views.submit_course_assessments'),
    url('getCourseAssessments/$', 'assessment.views.get_course_assessments'),
)
