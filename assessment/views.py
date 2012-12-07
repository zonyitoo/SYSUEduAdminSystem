# -*- coding:utf-8 -*-

from django.http import HttpResponseForbidden, HttpResponseBadRequest
from take.models import Takes
from course.models import Course
from student.models import Student
from assessment.models import Assessment
from ajaxutils.decorators import ajax

@ajax(login_required=True, require_GET=True)
def get_course_assessments(request):
    if not hasattr(request.user, 'administrator'):
        return HttpResponseForbidden('Only Administrator can do')

    year = request.GET['year']
    sem = int(request.GET['semester'])
    dept = request.GET['department']
    
    return {
        'assessments':
            [ass.getDataDict() for ass in Assessment.objects.filter(
                    course__semester__exact=sem,
                    course__academic_year__exact=year,
                    course__department__name__exact=dept
                )]
    }

