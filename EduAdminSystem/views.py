from django.http import HttpResponse, HttpResponseForbidden
from django.template import Template, Context, RequestContext
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

def helloworld(request):
    t = Template("This is a HelloWorld {{ person.firstname }}.")
    d = {"person": {"firstname": "Joe", "lastname": "Johnson"}}
    return HttpResponse(t.render(Context(d)))

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
