from django.conf.urls import patterns, url

urlpatterns = patterns('', 
    url('login/$', 'user.views.login_page'), 
    url('logout/$', 'user.views.do_logout'), 
    url('modifypwd/$', 'user.views.modify_pwd'),
)
