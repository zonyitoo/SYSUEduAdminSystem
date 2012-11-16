from django.http import HttpResponse
from user.controller import *
from school.models import *
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response

def login(request):
    return render_to_response('login.html', {}, context_instance=RequestContext(request))

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
    
