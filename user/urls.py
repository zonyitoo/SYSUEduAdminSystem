from django.conf.urls import patterns, include, url

urlpatterns = patterns('', 
    url('adduser/$', 'user.views.add_user'), 
    url('loadimg/$', 'user.views.show_pic'),  
    url('login/$', 'user.views.login'), 
)
