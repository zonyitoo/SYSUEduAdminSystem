from django.conf.urls import patterns, url

urlpatterns = patterns('', 
    url('getAvailableList/$', 'course.views.get_available_list'), 
)
