# -*- coding:utf-8 -*-

from django.http import HttpResponseForbidden
from take.models import Takes
from course.models import Course
from models import Student
from ajaxutils.decorators import ajax

@ajax(login_required=True, require_POST=True)
def select_course(request):
    if request.method == 'POST':
        if not hasattr(request.user, 'student'):
            return HttpResponseBadRequest('Only Student can select course')

        course_id = request.POST['course_id']
        course = None
        try:
            course = Course.objects.get(id=int(course_id))
        except:
            return HttpResponse(simplejson.dumps({'valid':False,  'error_msg':
                '该课程不存在'}), mimetype='application/json')

        student = Student.objects.get(user=request.user)
        try:
            take = Takes.objects.create(course=course,student=student)
            take.save()
        except:
            pass

        return HttpResponse(simplejson.dumps({'valid': True,
            'hastaken':Takes.objects.filter(course=course,student=student).count()}),
            mimetype='application/json')

    else:
        return HttpResponseBadRequest('Invalid Method')

@ajax(login_required=True, require_POST=True)
def withdrawal_course(request):
    if not hasattr(request.user, 'student'):
        return HttpResponseForbidden('Only Student can withdrawal')

    course_id = request.POST['course_id']
    course = None
    try:
        course = Course.objects.get(id=int(course_id))
    except:
        return HttpResponseForbidden('该课程不存在')

    student = Student.objects.get(user=request.user)
    try:
        take = Takes.objects.get(course=course, student=student)
        take.delete()
    except:
        pass
    
    return {'valid': True, 
        'hastaken': Takes.objects.filter(course=course, student=student).count()}
    
