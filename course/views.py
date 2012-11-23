from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from course.models import CourseType
from django.utils import simplejson

coursetype = {
        'po': CourseType.PUB_ELECTIVE, 
        'pr': CourseType.PUB_COURSE,
        'mo': CourseType.PRO_ELECTIVE,
        'mr': CourseType.PRO_COURSE
        }

@login_required
def get_avaliable_list(request):
    if request.method == 'GET':
        caltivate = request.GET.get('cultivate', 0)
        ct = coursetype[request.GET.get('', 'po')]
        
        ## JUST for test, return from get
        return HttpResponse(simplejson.dumps(request.GET),
                mimetype='application/json')
