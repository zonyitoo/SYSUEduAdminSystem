from django.conf.urls import patterns, include, url

urlpatterns = patterns('', 
    url('login/$', 'user.views.login_page'), 
    url('logout/$', 'user.views.do_logout'), 
)
