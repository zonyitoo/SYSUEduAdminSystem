from django.conf.urls import patterns, include, url

urlpatterns = patterns('', 
        url(r'getTakenInfoList/$', 'teacher.views.get_takeninfo_list'),
)
