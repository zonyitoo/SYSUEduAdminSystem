from django.http import (
    HttpResponseNotAllowed, HttpResponseRedirect, HttpResponse,
    HttpResponseBadRequest
)
from user.controller import *
from school.models import *
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.core.context_processors import csrf
from django.contrib.auth import authenticate, login, logout
from django.utils import simplejson
from ajaxutils.decorators import ajax

def login_page(request):
    if request.method == 'GET':
        args = {'next': request.GET.get('next', '/')}
        # If has login
        if not request.user.is_anonymous():
            return HttpResponseRedirect(args['next'])
        
        # if logout
        if 'logoutid' in request.GET:
            logoutaccount = request.GET['logoutid']
            args['logoutaccount'] = logoutaccount

        args.update(csrf(request))
        return render_to_response('login_extern.html', args, 
                context_instance=RequestContext(request))
    # do login
    elif request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('passwd', '')
        user = authenticate(username=username, password=password)
        retjson = {}
        if user is None:
            retjson['valid'] = False
            return HttpResponse(simplejson.dumps(retjson),
                mimetype='application/json')
        else:
            login(request, user)
            retjson['valid'] = True

        # Admin User (for test)
        if user.is_superuser:
            retjson['next'] = '/admin/'
            return HttpResponse(simplejson.dumps(retjson),
                mimetype='application/json')

        # Normal User
        retjson['next'] = request.POST.get('next', '/')
        return HttpResponse(simplejson.dumps(retjson),
            mimetype='application/json')
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

@ajax(login_required=True, require_POST=True)
def do_logout(request):
    tojson = {}
    if not request.user.is_anonymous():
        tojson['logoutaccount'] = request.user.username

    logout(request)
    return tojson

@ajax(login_required=True, require_POST=True)
def modify_pwd(request):
    try:
        oldpasswd = request.POST['oldpasswd']
        newpasswd = request.POST['newpasswd']
    except:
        return HttpResponseBadRequest('Invalid Arguments')

    if not request.user.check_password(oldpasswd):
        return {'valid': False}
    else:
        request.user.set_password(newpasswd)
        request.user.save()
        return {'valid': True}
