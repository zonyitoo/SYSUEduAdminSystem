# -*- coding:utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import simplejson
from take.models import Takes
from course.models import Course
from models import Student

@login_required
def select_course(request):
    pass

@login_required
def withdrawal_course(request):
    if request.method == 'POST':
        if not hasattr(request.user, 'student'):
            return HttpResponseBadRequest('Only Student can withdrawal')

        course_id = request.POST['course_id']
        course = None
        try:
            course = Course.objects.get(id=int(course_id))
        except:
            return HttpResponse(simplejson.dumps({'valid': False, 'error_msg':
                '该课程不存在'}), mimetype='application/json')

        student = Student.objects.get(user=request.user)
        try:
            take = Takes.objects.get(course=course, student=student)
            take.delete()
        except:
            pass
        
        return HttpResponse(simplejson.dumps({'valid': True, 
            'hastaken': Takes.objects.filter(course=course, student=student).count()}), 
            mimetype='application/json')

    else:
        return HttpResponseBadRequest('Invalid Method')
