from django.conf.urls import patterns, include, url

urlpatterns = patterns('', 
        url(r'getTakenInfoList/$', 'teacher.views.get_takeninfo_list'),
        url(r'getScoreableList/$', 'teacher.views.get_scoreable_list'),
        url(r'getScoreSheet/(.*.xls)$', 'teacher.views.get_score_sheet'),
        url(r'uploadScoreSheet/$', 'teacher.views.upload_score_sheet'),
)
