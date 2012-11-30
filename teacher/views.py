# -*- coding:utf-8 -*-
from django.http import (
    HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
)
from ajaxutils.decorators import ajax

from course.models import Course, CourseType
from teacher.models import Teacher
from take.models import Takes
import time, xlwt, random, os

@ajax(login_required=True, require_GET=True)
def get_scoreable_list(request):
    if not hasattr(request.user, 'teacher'):
        return HttpResponseForbidden("Only teacher can access")

    t = time.localtime(time.time())
    year = t.tm_year
    month = t.tm_mon
    if month >= 9 or month <= 1:
        year = str(year) + '-' + str(year + 1)
    else:
        year = str(year - 1) + '-' + str(year)

    courses = Course.objects.filter(
                teacher__user__exact=request.user,
                academic_year=year
            )

    return {
        'courses': [course.name for course in courses],
        'year': year
    }
    
@ajax(login_required=True, require_GET=True)
def get_takeninfo_list(request):
    if not hasattr(request.user, 'teacher'):
        return HttpResponseForbidden("Only teacher can access")

    course = request.GET['course']

    takes = Takes.objects.filter(course__name__exact=course)

    return {
        'takes': [take.getDataDict() for take in takes],
    }
    
@ajax(login_required=True, require_GET=True)
def get_score_sheet(request):
    if not hasattr(request.user, 'teacher'):
        return HttpResponseForbidden("Only teacher can do this")

    t = time.localtime(time.time())
    year = t.tm_year
    month = t.tm_mon
    if month >= 9 or month <= 1:
        year = str(year) + '-' + str(year + 1)
    else:
        year = str(year - 1) + '-' + str(year)

    takes = Takes.objects.filter(
            course__name__exact=request.GET['course'],
            course__academic_year__exact=year,
            course__teacher__user__exact=request.user
        ).order_by('student__user__username')

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('scores')
    sheet.write(0, 0, u'学号')
    sheet.write(0, 1, u'姓名')
    sheet.write(0, 2, u'平时成绩')
    sheet.write(0, 3, u'期末成绩')
    sheet.write(0, 4, u'出席率（0-100）')

    row = 1
    for take in takes:
        sheet.write(row, 0, take.student.user.username)
        sheet.write(row, 1, take.student.student_name)
        row += 1

    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachments; filename=scores.xls'
    workbook.save(response)

    return response
    
@ajax(login_required=True, require_POST=True)
def upload_score_sheet(request):
    pass
