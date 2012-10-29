from django.http import HttpResponse
from django.template import Template, Context

def helloworld(request):
    t = Template("This is a HelloWorld {{ person.firstname }}.")
    d = {"person": {"firstname": "Joe", "lastname": "Johnson"}}
    return HttpResponse(t.render(Context(d)))
