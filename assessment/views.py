# -*- coding:utf-8 -*-

from django.http import HttpResponseForbidden, HttpResponseBadRequest
from take.models import Takes
from course.models import Course
from student.models import Student
from ajaxutils.decorators import ajax

@ajax(login_required=True, require_GET=True)
def get_course_assessment(request):
    if not hasattr(request.user, 'administrator'):
        return HttpResponseForbidden('Only Administrator can do')

    course = request['course']

