from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'EduAdminSystem.views.home', name='home'),
    # url(r'^EduAdminSystem/', include('EduAdminSystem.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^test/', 'EduAdminSystem.views.helloworld'), 
    url(r'^user/', include('user.urls')), 
    url(r'^$', 'EduAdminSystem.views.index'), 
    url(r'^student/$', 'user.views.student_page'), 
)
