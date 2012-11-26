# -*- coding:utf-8 -*-

from django.http import HttpResponseForbidden, HttpResponseBadRequest
from take.models import Takes
from course.models import Course
from models import Student
from ajaxutils.decorators import ajax

def select_course(request):
    if not hasattr(request.user, 'student'):
        return HttpResponseForbidden('Only Student can select course')

    course_id = request.POST['course_id']
    course = None
    try:
        course = Course.objects.get(id=int(course_id))
    except:
        return HttpResponseForbidden('该课程不存在')

    student = Student.objects.get(user=request.user)
    try:
        take = Takes.objects.create(course=course,student=student)
        take.save()
    except:
        pass

    return {'valid': True,
        'hastaken':Takes.objects.filter(course=course,student=student).count()}

def withdrawal_course(student, course):
    try:
        take = Takes.objects.get(course=course, student=student)
        take.delete()
    except:
        pass
    
    return {'valid': True, 
        'hastaken': Takes.objects.filter(course=course, student=student).count()}
    
@ajax(login_required=True, require_POST=True)
def toggle_course(request):
    student = Student.object.get(user=request.user)
    try:
        course = Course.objects.get(id=int(request.POST['course_id']))
    except Course.DoesNotExist:
        return HttpResponseForbidden('该课程不存在')

    if request.POST['state'] == '1':
        select_course(student, course)
    elif request.POST['state'] == '0':
        withdrawal_course(student, course)
    else:
        return HttpResponseBadRequest('Invalid Command')
