# -*- coding:utf-8 -*-
from django.http import (
    HttpResponseForbidden, HttpResponseBadRequest, HttpResponse
)
from globaldata.models import GlobalData
from take.models import Takes
from course.models import Course
from student.models import Student, StudentMeta
from teacher.models import Teacher
from school.models import Department, Speciality
from django.contrib.auth.models import User, Group, Permission
from ajaxutils.decorators import ajax
import time, xlwt, xlrd

import logging
logger = logging.getLogger('EduAdminSystem')

COURSE_TYPE = [
    'PUB_ELECTIVE',
    'PUB_COURSE',
    'PRO_ELECTIVE',
    'PRO_COURSE',
    'GYM_ELECTIVE',
]

C_TYPE = [
    Course.PUB_ELECTIVE,
    Course.PUB_COURSE,
    Course.PRO_ELECTIVE,
    Course.PRO_COURSE,
    Course.GYM_ELECTIVE,
]

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
                    user.set_password(row[2][-6:])
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
                try:
                    stud = Student.objects.get(student_name=row[1], user=user)
                    if stud.student_meta is not meta:
                        stud.student_meta = meta
                        stud.save()
                except Student.DoesNotExist:
                    stud = Student(student_name=row[1], user=user,
                            student_meta=meta)
                    stud.save()

    except xlrd.XLRDError:
        return HttpResponseBadRequest('xls file error')
    except:
        return HttpResponseBadRequest('Error occur')

    return {
        'valid': True,
    }
        
@ajax(login_required=True, require_GET=True)
def get_teacher_sheet(request, filename):
    ## Make all the departments of a school. Every department a sheet
    workbook = xlwt.Workbook()
    departs =\
        Department.objects.filter(school__name__exact=request.GET['school'])

    for depart in departs:
        sheet = workbook.add_sheet(depart.name)
        sheet.write(0, 0, u'登录名')
        sheet.write(0, 1, u'姓名')
        sheet.write(0, 2, u'身份证号')
        sheet.write(0, 3, u'学系')
        sheet.write(1, 0, u'jqg')
        sheet.write(1, 1, u'纪老师')
        sheet.write(1, 2, u'4007820000000000')
        sheet.write(1, 3, u'计算机科学系')

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachments'
    workbook.save(response)

    return response

@ajax(login_required=True, require_POST=True)
def upload_teacher_sheet(request):
    fileobj = request.FILES['file']

    try:
        wb = xlrd.open_workbook(file_contents=fileobj.read())
        for sheet in wb.sheets():
            for rid in range(1, sheet.nrow):
                row = sheet.row_values(rid)
                depart = Department.objects.get(name=row[3])
                try:
                    user = User.objects.get(username=row[0])
                    user.set_password(row[2][-6:])
                except:
                    user = User.objects.create_user(username=row[0], 
                            password=row[2][-6:])

                Teacher.objects.get_or_create(teacher_name=row[1], 
                        department=depart)[0].save()

    except xlrd.XLRDError:
        return HttpResponseBadRequest('xls file error')
    except:
        return HttpResponseBadRequest('error occur')

    return {'valid': True}

@ajax(login_required=True, require_GET=True)
def get_select_course_state(request):
    usergrp = Group.objects.get(name='student')
    perm = Permission.objects.get(codename='add_takes')

    if perm in usergrp.permissions.all():
        return {'state': True}
    else:
        return {'state': False}

@ajax(login_required=True, require_POST=True)
def open_select_course(request):
    if not hasattr(request.user, 'administrator'):
        return HttpResponseForbidden('Only Administrator can do')

    usergrp = Group.objects.get(name='student')
    perm = Permission.objects.get(codename='add_takes')
    
    ## Open
    if not perm in usergrp.permissions.all():
        usergrp.permissions.add(perm)

    return {'success': True, 'state': True}

@ajax(login_required=True, require_POST=True)
def close_select_course(request):
    if not hasattr(request.user, 'administrator'):
        return HttpResponseForbidden('Only Administrator can do')

    usergrp = Group.objects.get(name='student')

    try:
        usergrp.permissions.get(codename='add_takes').delete()
    except Permission.DoesNotExist:
        pass

    return {'success': True, 'state': False}

@ajax(login_required=True, require_POST=True)
def toggle_course_screen(request):
    c_type = COURSE_TYPE[int(request.POST['course_type'])]
    cc_type = C_TYPE[int(request.POST['course_type'])]
    stage = GlobalData.objects.filter(name=c_type) 
    if stage[0].stage == 1 or stage[0].stage == 2 :
        course = Course.objects.filter(course_type=cc_type,screened=False)
        for c in course:
            already_taken = Takes.objects.filter(course=c,screened=True)
            already_taken_num = already_taken.count()

            take = Takes.objects.filter(course=c,screened=False)
            wait_for_screen = take.count()

            avail_num_max = c.capacity - already_taken_num
            screen_num = min(avail_num_max,wait_for_screen)
            if screen_num>0 :
                take = take.order_by('?')[:screen_num]
                for t in take:
                    t.screened = True
                    t.save()
            
            not_take = Takes.objects.filter(course=c,screened=False)
            for n in not_take:
                n.delete()


            c.hastaken = already_taken_num + screen_num
            c.save()
        
        for s in stage:
            s.stage += 1
            s.save()

    elif stage[0].stage  == 3:
        c_type = COURSE_TYPE[int(request.POST['course_type'])]
        cc_type = C_TYPE[int(request.POST['course_type'])]
        course = Course.objects.filter(course_type=cc_type,stage=stage,screened=False)
        for c in course:
            c.screened = True
            c.save()

    return {'valid': True}

@ajax(login_required=True, require_POST=True)
def open_upload_score(request):
    if not hasattr(request.user, 'administrator'):
        return HttpResponseForbidden('Only Administrator can do')
    
    usergrp = Group.objects.get(name='teacher')
    perm = Permission.objects.get(codename='change_takes')

    if not perm in usergrp.permissions.all():
        usergrp.permissions.add(perm)

    return {'success': True, 'state': True}

    
@ajax(login_required=True, require_POST=True)
def close_upload_score(request):
    if not hasattr(request.user, 'administrator'):
        return HttpResponseForbidden('Only Administrator can do')

    usergrp = Group.objects.get(name='teacher')

    try:
        usergrp.permissions.get(codename='change_takes').delete()
    except Permission.DoesNotExist:
        pass

    return {'success': True, 'state': False}

@ajax(login_required=True, require_GET=True)
def get_upload_score_state(request):
    usergrp = Group.objects.get(name='teacher')
    perm = Permission.objects.get(codename='change_takes')

    return {'state': perm in usergrp.permissions.all()}
