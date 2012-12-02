# -*- coding:utf-8 -*-
from django.http import (
    HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
)
from take.models import Takes
from course.models import Course
from student.models import Student
from school.models import Department
from ajaxutils.decorators import ajax
import time, xlwt, xlrd

@ajax(login_required=True, require_GET=True)
def get_student_sheet(request, filename):
    t = time.localtime(time.time())
    year = t.tm_year
    month = t.tm_mon
    if month >= 9 or month <= 1:
        year = str(year) + '-' + str(year + 1)
    else:
        year = str(year - 1) + '-' + str(year)

    ## Make all the departments. Every department a sheet
    workbook = xlwt.Workbook()
    departs = Department.objects.all()
    for depart in departs:
        sheet = workbook.add_sheet(depart.name)
        sheet.write(0, 0, year)
        sheet.write(0, 1, u'公共必修总学分')
        sheet.write(0, 2, 10)
        sheet.write(0, 3, u'公共选修总学分')
        sheet.write(0, 4, 20)
        sheet.write(0, 5, u'专业必修总学分')
        sheet.write(0, 6, 30)
        sheet.write(0, 7, u'专业选修总学分')
        sheet.write(0, 8, 40)
        sheet.write(1, 0, u'学号')
        sheet.write(1, 1, u'姓名')
        sheet.write(1, 2, u'专业')
        sheet.write(2, 0, u'10383001')
        sheet.write(2, 1, u'张三')
        sheet.write(2, 2, u'计算机科学与技术')

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachments'
    workbook.save(response)

    return response

def upload_student_sheet(request):
    pass
