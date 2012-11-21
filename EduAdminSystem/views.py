#-*- coding=utf-8 -*-

from django.http import HttpResponse, HttpResponseForbidden
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from user.controller import create_student
from school.models import *

def helloworld(request):
    sist = School(name='SIST', addr='FUCK')
    sist.save()
    cs = Department(name='CS', addr='YOU', school=sist)
    cs.save()
    cst = Speciality(name='CST', department=cs)
    cst.save()

    create_student('10383007', u'零零七', '123456', 'UG', '2010', 'CST')
    
    return HttpResponse('Inserted 10383007, password is 123456')

def copyright(request):
    return HttpResponse("Copyrighted by iphkwan, the19thell, zonyitoo, sheepke.")

@login_required(login_url='/user/login/')
def index(request):
    if request.method == "GET":
        if hasattr(request.user, 'student'):
            return render_to_response('student.html', {},
                context_instance=RequestContext(request))
        elif hasattr(request.user, 'teacher'):
            pass
        else:
            return HttpResponseForbidden('Admin User??' + request.user.username)
    else:
        return HttpResponseForbidden('Invalid method')
