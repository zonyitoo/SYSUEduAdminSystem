# -*- coding:utf-8 -*-
from django.http import (
    HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
)
from take.models import Takes
from course.models import Course
from student.models import Student, StudentMeta
from school.models import Department, Speciality
from django.contrib.auth.models import User, Group
from ajaxutils.decorators import ajax
import time, xlwt, xlrd

import logging
logger = logging.getLogger('EduAdminSystem')

@ajax(login_required=True, require_GET=True)
def get_student_list(request):
    school = request.GET['school']

    return {
        'students': [stud.getDataDict() for stud in
            Student.objects.filter(student_meta__major__department__school__name__exact=school)]
    }

@ajax(login_required=True, require_GET=True)
def get_student_sheet(request, filename):
    t = time.localtime(time.time())
    year = t.tm_year
    ## Make all the departments of a school. Every department a sheet
    workbook = xlwt.Workbook()
    departs =\
        Department.objects.filter(school__name__exact=request.GET['school'])

    for depart in departs:
        sheet = workbook.add_sheet(depart.name)
        sheet.write(0, 0, unicode(year))
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
        sheet.write(1, 2, u'身份证号')
        sheet.write(1, 3, u'专业')
        sheet.write(2, 0, u'10383001')
        sheet.write(2, 1, u'张三')
        sheet.write(2, 2, u'4007820000000000')
        sheet.write(2, 3, u'计算机科学与技术')

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachments'
    workbook.save(response)

    return response

@ajax(login_required=True, require_POST=True)
def upload_student_sheet(request):
    fileobj = request.FILES['file']
    exilst = []
    try:
        wb = xlrd.open_workbook(file_contents=fileobj.read())
        for sheet in wb.sheets():
            depart = Department.objects.get(name=sheet.name)
            frow = sheet.row_values(0)
            year = frow[0]
            req_pubcourse = frow[2]
            req_pubelective = frow[4]
            req_procourse = frow[6]
            req_proelective = frow[8]

            for rind in range(2, sheet.nrows):
                row = sheet.row_values(rind)
                spec = Speciality.objects.get_or_create(
                            name=row[3],
                            department=depart
                        )
                if spec[1]:
                    spec[0].save()

                try:
                    user = User.objects.get(username=row[0])
                    exilst.append({
                            'number': row[0],
                            'name': row[1]
                        })
                    continue
                except User.DoesNotExist:
                    user = User.objects.create_user(username=row[0],
                            password=row[2][-6:])
                    user.save()

                meta = StudentMeta.objects.get_or_create(
                            year=year,
                            req_pubcourse=req_pubcourse,
                            req_pubelective=req_pubelective,
                            req_procourse=req_procourse,
                            req_proelective=req_proelective,
                            major=spec[0]
                        )[0]
                s = Student(student_name=row[1], student_meta=meta,
                        user=user)
                s.save()
    except xlrd.XLRDError:
        return HttpResponseBadRequest('xls file error')
    except:
        return HttpResponseBadRequest('Error occur')

    return {
        'valid': True,
        'exist_list': exilst,
    }
        
@ajax(login_required=True, require_POST=True)
def toggle_select_course(request):
    usergrp = Group.objects.get(name='student')
    
    state = request.POST['state']
    if state == '1':
        if usergrp.has_perm('add_takes'):
            pass
    elif state == '2':
        pass

