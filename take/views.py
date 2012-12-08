# -*- coding:utf-8 -*-
from ajaxutils.decorators import ajax
from take.models import Takes

@ajax(login_required=True, require_GET=True)
def get_take_courses(request):
    year = request.GET.get('school-year', '')
    sem = request.GET.get('school-term', '')

    user = request.user
    
    takes = Takes.objects.filter(student__user__exact=user,
            course__academic_year__exact=year,
            course__semester__exact=sem)
       
    courseArr = [take.course.getDataDict() for take in takes]

    return {
        'courses': courseArr, 
        'studentid': request.user.username
    }

@ajax(login_required=True, require_GET=True)
def get_take_score(request):
    year = request.GET.get('school-year', '')
    sem = int(request.GET.get('school-term', '1'))

    user = request.user
    
    takes = Takes.objects.filter(student__user__exact=user,
            course__academic_year__exact=year,
            course__semester__exact=sem, has_assessment=True)
    
    takeArr = [take.getDataDict() for take in takes]
    return {
            'takes': takeArr,
        'studentid': request.user.username
    }

@ajax(login_required=True, require_GET=True)
def get_take_assessment(request):
    takes = Takes.objects.filter(student__user__exact=request.user,
            has_assessment=False)

    takeArr = [take.getDataDict() for take in takes]
    return {
            'assessment': takeArr,
            'studentid': request.user.username
            }
