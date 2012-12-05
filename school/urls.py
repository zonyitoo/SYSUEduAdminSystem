from django.conf.urls import patterns, url

urlpatterns = patterns('', 
            url('getAllSchools/$', 'school.views.get_all_schools'),
            url('getAllDepartments/$', 'school.views.get_all_departments'),
            url('getAllSpecialities/$', 'school.views.get_all_specialities'),
        )
