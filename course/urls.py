from django.conf.urls import patterns, url

urlpatterns = patterns('', 
    url('getAvaliableList/$', 'course.views.get_avaliable_list'), 
)
