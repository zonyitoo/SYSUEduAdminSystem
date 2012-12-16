# -*- coding:utf-8 -*-

from django.http import HttpResponseForbidden, HttpResponseBadRequest
from take.models import Takes
from course.models import Course
from student.models import Student
from assessment.models import Assessment, AssessmentSubject, AssessmentEntry
from django.db.models import Count
from ajaxutils.decorators import ajax
import time

@ajax(login_required=True, require_GET=True)
def get_assessment_entries(request):
    try:
        ass_type = request.GET['assessment_type']
    except:
        return HttpResponseBadRequest('Invalid Arguments')
    
    ass_type = int(ass_type)

    subjs = AssessmentSubject.objects.filter(assessment_type=ass_type)
    
    result = []
    for subject in subjs:
        result.append({
            'subject': subject.getDataDict(),
            'entries': [entry.getDataDict()
                for entry in AssessmentEntry.objects.filter(subject=subject)]
        })

    return {
        'assessments': result,
    }

@ajax(login_required=True, require_GET=True)
def get_course_assessments(request):
    if not hasattr(request.user, 'administrator'):
        return HttpResponseForbidden('Only Administrator can do')

    t = time.localtime(time.time())
    year = t.tm_year
    month = t.tm_mon
    if month >= 9 or month <= 1:
        year = str(year) + '-' + str(year + 1)
    else:
        year = str(year - 1) + '-' + str(year)

    if month >= 9 or month <= 1:
        sem = 1
    elif month > 1 and month <= 6:
        sem = 2
    else:
        sem = 3
    try:
        dept = request.GET['department']
        course_name = request.GET['course_name']
    except:
        return HttpResponseBadRequest('Invalid Arguments')
    
    try:
        course = Course.objects.get(semester__exact=sem,
                academic_year=year, department__name__exact=dept,
                name=course_name)
    except Course.DoesNotExist:
        return HttpResponseBadRequest('Course DoesNotExist')
    
    return {
        'assessments':
            [ass.getDataDict() for ass in Assessment.objects.filter(
                    course=course)]
    }
    
@ajax(login_required=True, require_GET=True)
def get_assessments(request):
    if not hasattr(request.user, 'administrator'):
        return HttpResponseForbidden('Only Administrator can do')

    try:
        department = request.GET['department']
        year = request.GET['year']
        sem = request.GET['semester']
    except:
        return HttpResponseBadRequest('Invalid Argument')

    courses = Course.objects.filter(department__name__exact=department,
            academic_year=year, semester=sem)

    result = []
    for course in courses:
        asses = Assessment.objects.filter(course=course)
        total = 0
        for ass in asses:
            total += ass.score * ass.entry.weight
        result.append({
                'course': course.getDataDict(),
                'assessment_score': total,
            })

    return {'assessments': result}

@ajax(login_required=True, require_POST=True)
def submit_course_assessments(request):
    if not hasattr(request.user, 'student'):
        return HttpResponseForbidden('Only Student can do')

    try:
        dept = request.POST['department']
        course_name = request.POST['course_name']
        ass_score = request.POST['score'].split(',')
    except:
        return HttpResponseBadRequest('Invalid arguments')

    t = time.localtime(time.time())
    year = t.tm_year
    month = t.tm_mon
    if month >= 9 or month <= 1:
        year = str(year) + '-' + str(year + 1)
    else:
        year = str(year - 1) + '-' + str(year)

    if month >= 9 or month <= 1:
        sem = 1
    elif month > 1 and month <= 6:
        sem = 2
    else:
        sem = 3

    try:
        course = Course.objects.get(name__exact=course_name, 
                semester__exact=sem,
                academic_year=year, 
                department__name__exact=dept)
    except Course.DoesNotExist:
        return HttpResponseBadRequest('Course DoesNotExist')

    try:
        subjects = AssessmentSubject.objects.filter(
                assessment_type=course.assessment_type
            ).order_by('id')

        score_ind = 0;
        for subj in subjects:
            entries =\
                AssessmentEntry.objects.filter(subject=subj).order_by('id')
            for entry in entries:
                ass = Assessment.objects.get_or_create(course=course, 
                        entry=entry)[0]
                ass.score = ass_score[score_ind]
                score_ind += 1
                ass.save()

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
