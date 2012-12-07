# -*- coding:utf-8 -*-

from django.http import HttpResponseForbidden, HttpResponseBadRequest
from take.models import Takes
from course.models import Course
from student.models import Student
from ajaxutils.decorators import ajax

# a simple version of course time collision detect
def time_collision_detect(student, course):

    # the filter can be optimized by adding academic_year?
    takes = Takes.objects.filter(student=student)
    for t in takes:
        # have chosen this course before, return err 401
        if t.course.name == course.name:
            return 41
        # different sem or academic year, pass
        elif t.course.academic_year == course.academic_year and t.course.semester == course.semester:
            cta = t.course.course_time.all()
            ctb = course.course_time.all()
            #course time collision check, if found, return err 402
            for ta in cta:
                stra = ta.time
                weeka = ta.week
                for tb in ctb:
                    strb = tb.time
                    weekb = tb.week
                    for ch in stra:
                        if strb.find(ch) != -1 and weeka == weekb:
                            return 42
    return 20

def course_capacity_detect(course):
    if course.capacity <= course.hastaken and course.stage == 3:
        # if it's full and it's in third stage, return err 403
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
    if not request.user.has_perm('add_takes'):
        #If admin close the permission
        pass

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

