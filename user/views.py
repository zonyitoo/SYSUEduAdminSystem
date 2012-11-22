from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from user.controller import *
from school.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout

def login_page(request):
    if request.method == 'GET':
        args = {'next': request.GET.get('next', '/')}
        # If has login
        if not request.user.is_anonymous():
            return HttpResponseRedirect(args['next'])

        args.update(csrf(request))
        return render_to_response('login.html', args, 
                context_instance=RequestContext(request))
    # do login
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('passwd', '')
        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponseBadRequest('Invalid username or password. POST\
                    username=%s,passwd=%s' % (username, password))
        else:
            login(request, user)
	    if user.is_staff :
		return HttpResponseRedirect("/admin/")
            #return HttpResponseRedirect('/')
            return HttpResponseRedirect(request.POST.get('next', '/'))
	    #return student_page(request)
    else:
        return HttpResponseBadRequest('Invalid method')

def student_page(request):
    if request.method == 'GET':
        return render_to_response('student.html', {},
                    context_instance=RequestContext(request))
   
def do_logout(request):
    logout(request)
    return HttpResponseRedirect('/user/login/')
