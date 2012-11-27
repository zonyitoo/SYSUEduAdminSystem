from django.conf.urls import patterns, url

urlpatterns = patterns('', 
    url('getAvailableList/$', 'course.views.get_available_list'), 
    url('getEducatePlan/$', 'course.views.get_educate_plan'),
)
