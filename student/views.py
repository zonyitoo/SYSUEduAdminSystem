# -*- coding:utf-8 -*-

from django.http import HttpResponseForbidden, HttpResponseBadRequest
from take.models import Takes
from course.models import Course
from models import Student
from ajaxutils.decorators import ajax

def select_course(request):
    pass

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
