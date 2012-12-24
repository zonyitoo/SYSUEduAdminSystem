# -*- coding:utf-8 -*-

from django.http import HttpResponseForbidden, HttpResponseBadRequest
from globaldata.models import GlobalData
from take.models import Takes
from course.models import Course
from student.models import Student
from ajaxutils.decorators import ajax
from django.contrib.auth.models import Group, Permission
C_TYPE = {
        'PubE':'PUB_ELECTIVE',
        'PubC':'PUB_COURSE',
        'ProE':'PRO_ELECTIVE',
        'ProC':'PRO_COURSE',
        'GymE':'GYM_ELECTIVE'
}

# a simple version of course time collision detect
def time_collision_detect(student, course, stage):

    # the filter can be optimized by adding academic_year?
    takes = Takes.objects.filter(student=student)
    PubECount = 0
    GYMECount = 0
    for t in takes:
        # have chosen this course before, return err 41
        if t.course.name == course.name:
            return 41
        # different sem or academic year, pass
        elif t.course.academic_year == course.academic_year and t.course.semester == course.semester:
            if t.course.course_type == 'PubE':
                PubECount = PubECount + 1
            if t.course.course_type == 'GymE':
                GYMECount = GYMECount + 1
                # GYM course won't meet time collision
                continue
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
    if course.course_type == 'GymE':
        if stage == 3 and GYMECount == 1:
            # student should not choose more than 1 GymE_Course in one term
            return 45
        if stage < 3 and GYMECount == 4:
            return 46
    return 20

def course_capacity_detect(course,stage):
    if course.capacity <= course.hastaken and stage == 3 :
        # if it's full and it's in third stage, return err 43
        return 43
    return 20

def select_course(student, course, rank):
    try:
        c_type = C_TYPE[course.course_type]
        st = GlobalData.objects.get(name=c_type)
        stage = st.stage
        # test time collision
        num = time_collision_detect(student, course, stage)
        if num != 20:
            return {'valid': False,
                    'err': num}

        # test capacity full or not, it should only work after random selection
        num = course_capacity_detect(course,stage)
        if num != 20:
            return {'valid': False,
                    'err': num}
	
        take = Takes.objects.create(course=course, student=student, rank=rank)

        if stage == 3:
            take.screened = True

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
    rank = 0
    try:
        course = Course.objects.get(id=int(request.POST['course_id']))
        if course.course_type == 'GymE':
            rank = request.POST['rank']
    except Course.DoesNotExist:
        return HttpResponseForbidden('该课程不存在')


    if request.POST['state'] == '1':
        return select_course(student, course, rank)
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


