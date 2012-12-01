#-*- coding=utf-8 -*-

from django.http import (
    HttpResponse, HttpResponseForbidden,
    HttpResponseRedirect, HttpResponseBadRequest
)
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from school.models import *
from student.models import Student
from teacher.models import Teacher
from ajaxutils.decorators import ajax

@login_required
def index(request):
    if request.method == "GET":
        attr = {}
        if hasattr(request.user, 'student'):
            student = Student.objects.get(user=request.user)
            attr.update({'name' : student.student_name, 
                    'account' : request.user.username})
        elif hasattr(request.user, 'teacher'):
            teacher = Teacher.objects.get(user=request.user)
            attr.update({'name': teacher.teacher_name, 
                    'account' : request.user.username})
        else:
            pass    

        return render_to_response('index.html', attr,
                context_instance=RequestContext(request))

    else:
        return HttpResponseBadRequest('Invalid Method')

from teacher.upload import ScoreUploadForm

@ajax(login_required=True, require_GET=True)
def index_getview(request):
    if hasattr(request.user, 'student'):
        return render_to_response('student.html', {},
            context_instance=RequestContext(request))
    elif hasattr(request.user, 'teacher'):
        return render_to_response('teacher.html', {'form': ScoreUploadForm()},
            context_instance=RequestContext(request))
    else:
        return HttpResponseForbidden('Admin User??' + request.user.username)
