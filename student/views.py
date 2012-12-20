# -*- coding:utf-8 -*-

from django.http import HttpResponseForbidden, HttpResponseBadRequest
from globaldata.models import GlobalData
from take.models import Takes
from course.models import Course
from student.models import Student
from ajaxutils.decorators import ajax
from django.contrib.auth.models import Group, Permission


# a simple version of course time collision detect
def time_collision_detect(student, course):

    # the filter can be optimized by adding academic_year?
    takes = Takes.objects.filter(student=student)
    PubECount = 0
    for t in takes:
        # have chosen this course before, return err 41
        if t.course.name == course.name:
            return 41
        # different sem or academic year, pass
        elif t.course.academic_year == course.academic_year and t.course.semester == course.semester:
            if t.course.course_type == 'PubE':
                PubECount = PubECount + 1
            cta = t.course.course_time.all()
            ctb = course.course_time.all()
            #course time collision check, if found, return err 42
            for ta in cta:
                stra = ta.time
                weeka = ta.week
                for tb in ctb:
                    strb = tb.time
                    weekb = tb.week
                    for ch in stra:
                        if strb.find(ch) != -1 and weeka == weekb:
                            return 42
    if course.course_type == 'PubE' and PubECount == 2:
        # the student should not choose more than 2 PublicElective Course in
        # one term, return error 44
        return 44
    return 20

def course_capacity_detect(course):
    if course.capacity <= course.hastaken :
        # if it's full and it's in third stage, return err 43
        return 43
    return 20

def select_course(student, course):
    try:
        # test time collision
        num = time_collision_detect(student, course)
        if num != 20:
            return {'valid': False,
                    'err': num}

        # test capacity full or not, it should only work after random selection
        num = course_capacity_detect(course)
        if num != 20:
            return {'valid': False,
                    'err': num}
	
        take = Takes.objects.create(course=course, student=student)
        take.save()
        course.hastaken = Takes.objects.filter(course=course).count()
        course.save()
    except:
        pass

    return {'valid': True,
            'hastaken': course.hastaken}

def withdrawal_course(student, course):
    try:
        take = Takes.objects.get(course=course, student=student)
        take.delete()
        course.hastaken = Takes.objects.filter(course=course).count()
        course.save()
    except:
        pass
    
    return {'valid': True, 
        'hastaken': course.hastaken}
    
@ajax(login_required=True, require_POST=True)
def toggle_course(request):
    studgrp = Group.objects.get(name='student')
    perm = Permission.objects.get(codename='add_takes')

    if not perm in studgrp.permissions.all():
        #If admin close the permission
        return HttpResponseForbidden('未开放选课')

    student = Student.objects.get(user=request.user)
    try:
        course = Course.objects.get(id=int(request.POST['course_id']))
    except Course.DoesNotExist:
        return HttpResponseForbidden('该课程不存在')


    if request.POST['state'] == '1':
        return select_course(student, course)
    elif request.POST['state'] == '0':
        return withdrawal_course(student, course)
    else:
        return HttpResponseBadRequest('Invalid Command')

@ajax(login_required=True, require_GET=True)
def get_student_list(request):
    if not hasattr(request.user, 'administrator'):
        return HttpResponseForbidden('Only Administrator can do')

    school = request.GET['school']
    grade = request.GET['grade']

    return {
        'students': [stud.getDataDict() for stud in
            Student.objects.filter(student_meta__major__speciality__department__school__name__exact=school,
                student_meta__year__exact=grade).order_by('user__username')]
    }


