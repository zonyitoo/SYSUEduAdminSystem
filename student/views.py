# -*- coding:utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.utils import simplejson
from take.models import Takes
from course.models import Course
from models import Student

@login_required
def select_courses(request):
    pass

@login_required
def redrawal_courses(request):
    if request.method == 'POST':
        course_id = request.POST['id']
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

            return HttpResponse(simplejson.dumps({'valid': True}), mimetype='application/json')
        except:
            return HttpResponse(simplejson.dumps({'valid': False, 'error_msg':
                '未选该课程'}), mimetype='application/json')

    else:
        return HttpResponseBadRequest('Invalid Method')
