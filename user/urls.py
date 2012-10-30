from django.conf.urls import patterns, include, url

urlpatterns = patterns('', 
    url('adduser/$', 'user.views.add_user'), 
     
)
