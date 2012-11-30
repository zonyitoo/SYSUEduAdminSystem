from django.http import HttpResponseForbidden, HttpResponseBadRequest
from ajaxutils.decorators import ajax

from course.models import Course, CourseType
from teacher.models import Teacher
from take.models import Takes
import time

@ajax(login_required=True, require_GET=True)
def get_scoreable_list(request):
    if not hasattr(request.user, 'teacher'):
        return HttpResponseForbidden("Only teacher can access")

    t = time.localtime(time.time())
    year = t.tm_year
    month = t.tm_mon
    if month >= 9 or month <= 1:
        year = str(year) + '-' + str(year + 1)
    else:
        year = str(year - 1) + '-' + str(year)

    courses = Course.objects.filter(
                teacher__user__exact=request.user,
                academic_year=year
            )

    return {
        'courses': [course.name for course in courses],
        'year': year
    }
    
@ajax(login_required=True, require_GET=True)
def get_takeninfo_list(request):
    if not hasattr(request.user, 'teacher'):
        return HttpResponseForbidden("Only teacher can access")

    course = request.GET['course']

    takes = Takes.objects.filter(course__name__exact=course)

    return {
        'takes': [take.getDataDict() for take in takes],
    }
