# -*- coding:utf-8 -*-

from django.http import HttpResponseForbidden, HttpResponseBadRequest
from take.models import Takes
from course.models import Course
from student.models import Student
from assessment.models import Assessment
from ajaxutils.decorators import ajax

@ajax(login_required=True, require_GET=True)
def get_course_assessments(request):
    if not hasattr(request.user, 'administrator'):
        return HttpResponseForbidden('Only Administrator can do')

    year = request.GET['year']
    sem = int(request.GET['semester'])
    dept = request.GET['department']
    course_name = request.GET['course_name']
    
    course = Course.objects.get(semester__exact=sem,
            academic_year=year, department__name__exact=dept,
            name=course_name)
    
    return {
        'assessments':
            [ass.getDataDict() for ass in Assessment.objects.filter(
                    course=course)]
    }

@ajax(login_required=True, require_POST=True)
def submit_course_assessments(request):
    if not hasattr(request.user, 'student'):
        return HttpResponseForbidden('Only Student can do')

    try:
        year = request.POST['year']
        sem = int(request.POST['semester'])
        dept = request.POST['department']
        course_name = request.POST['course_name']
        ass_score = request.POST['score'].split(' ')
    except:
        return HttpResponseBadRequest('Invalid arguments')
    
    try:
            course = Course.objects.get(name__exact=course_name, 
                    semester__exact=sem,
                    academic_year=year, 
                department__name__exact=dept)
    except:
        return HttpResponseBadRequest('Invalid course')

    try:
        subj = 0
        for score in ass_score:
            ass = Assessment.objects.get(course=course, subject=subj)
            ass.score = int(score)
            ass.save()
            subj += 1
    except:
        return HttpResponseBadRequest('Invalid Assessment')
    
    take = Takes.objects.get(course=course, student__user__exact=request.user)
    take.has_assessment = True
    take.save()

    return {
        'valid': True,
        'assessments': [ass.getDataDict() 
            for ass in Assessment.objects.filter(course=course)],
    }
