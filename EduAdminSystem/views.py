from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import Template, Context

def helloworld(request):
    t = Template("This is a HelloWorld {{ person.firstname }}.")
    d = {"person": {"firstname": "Joe", "lastname": "Johnson"}}
    return HttpResponse(t.render(Context(d)))

def copyright(request):
    return HttpResponse("Copyrighted by iphkwan, the19thell, zonyitoo, sheepke.")

def index(request):
    if request.method == "GET":
        return HttpResponseRedirect('/user/login/')
    else:
        return HttpResponseForbidden('Invalid method')
