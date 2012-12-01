# -*- coding:utf-8 -*-
from django.http import (
    HttpResponse, HttpResponseForbidden, HttpResponseBadRequest
)
from ajaxutils.decorators import ajax

from course.models import Course, CourseType
from teacher.models import Teacher
from take.models import Takes
from student.models import Student
import time, xlwt, xlrd

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
def get_score_sheet(request, filename):
    if not hasattr(request.user, 'teacher'):
        return HttpResponseForbidden("Only teacher can do this")

    t = time.localtime(time.time())
    year = t.tm_year
    month = t.tm_mon
    course_name = request.GET['course']
    if month >= 9 or month <= 1:
        year = str(year) + '-' + str(year + 1)
    else:
        year = str(year - 1) + '-' + str(year)

    takes = Takes.objects.filter(
            course__name__exact=course_name,
            course__academic_year__exact=year,
            course__teacher__user__exact=request.user
        ).order_by('student__user__username')

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('scores')
    sheet.write(0, 0, course_name)
    sheet.write(0, 1, 
            Course.objects.get(
                        name__exact=course_name,
                        academic_year__exact=year,
                        teacher__user__exact=request.user).id)
    sheet.write(1, 0, u'学号')
    sheet.write(1, 1, u'姓名')
    sheet.write(1, 2, u'平时成绩')
    sheet.write(1, 3, u'期末成绩')
    sheet.write(1, 4, u'出勤率')

    row = 2
    for take in takes:
        sheet.write(row, 0, take.student.user.username)
        sheet.write(row, 1, take.student.student_name)
        sheet.write(row, 2, take.usual_score)
        sheet.write(row, 3, take.final_score)
        sheet.write(row, 4, take.attendance)
        row += 1

    response = HttpResponse(mimetype='application/ms-excel')
    response['Content-Disposition'] = 'attachments'
    #u'attachments; filename=中山大学学生成绩录入模板_' + course_name + u'.xls'
    workbook.save(response)

    return response
    
@ajax(login_required=True, require_POST=True)
def upload_score_sheet(request):
    """
        Only teacher can do!!!
    """
    fileobj = request.FILE['file']
    wb = xlrd.open_workbook('filename')

    ## Don't know where the file exist.
    ## TODO: get file from ajax

    try:
        sheet = wb.sheet_by_name('scores')
        course_id = int(sheet.cell_value(0, 1))
        for ri in range(2, sheet.nrows):
            row = sheet.row_values(ri)
            studnum = row[0]
            studname = row[1]
            usualscore = row[2]
            finalscore = row[3]
            presence = row[4]

            take = Takes.objects.get(
                        student__user__username__exact=studnum,
                        student__student_name__exact=studname,
                        course__id__exact=course_id
                    )

            take.usual_score = usualscore
            take.final_score = finalscore
            percentage = take.course.final_percentage / 100
            take.score = finalscore * percentage\
                + usualscore * (1 - percentage)
            take.presence = presence
            take.save()
            
    except xlrd.XLRDError:
        return HttpResponseBadRequest('xls file invalid')
    except:
        return HttpResponseBadRequest('Error occur')

    takes = Takes.objects.filter(
                course__id__exact=course_id
            ).order_by('score')

    rank = 1
    for take in takes:
        take.rank = rank
        take.save()
        rank += 1

    return {
        'valid': True,
    }
