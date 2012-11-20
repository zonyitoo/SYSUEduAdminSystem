from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from user.controller import *
from school.models import *
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth import authenticate

def login(request):
    if request.method == 'GET':
        return render_to_response('login.html', csrf(request), context_instance=RequestContext(request))
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('passwd', '')
        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponseBadRequest('Invalid username or password')
        else:
            return HttpResponseRedirect('/student')
    else:
        return HttpResponseBadRequest('Invalid method')

def student_page(request):
    if request.method == 'GET':
        return render_to_response('student.html', {},
                    context_instance=RequestContext(request))


def show_pic(request):
    return render_to_response('login.html', {}, context_instance=RequestContext(request))

def add_user(request):
    number = request.GET.get('number', '')
    name = request.GET.get('name', '')
    password = request.GET.get('password', '')
    edutype = request.GET.get('edutype', 'UG')
    year = request.GET.get('year', '2010')
    speciality = request.GET.get('speciality', 'Comp.Sci.And.Tech.')

    create_student(number=number, name=name, password=password, edutype=edutype, year=year, speciality=speciality)
   
    return HttpResponse("number is %s, name is %s has been created" % (number, name))

def add_user_f(request):
    sch = School(name='SIST', addr="fuck")
    sch.save()
    dept = Department(name='Comp.Sci.', addr='DAMN', school=sch)
    dept.save()
    spe = Speciality(name='Comp.Sci.And.Tech.', department=dept)
    spe.save()

    return HttpResponse("DONE")
    
