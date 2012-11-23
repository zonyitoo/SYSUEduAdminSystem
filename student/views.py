from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

@login_required
def select_courses(request):
    pass

@login_required
def redrawal_courses(request):
    pass
