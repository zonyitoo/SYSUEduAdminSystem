# -*- coding:utf-8 -*-
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from student.models import Student
from course.models import Course, CourseType
from django.utils import simplejson

@login_required
def get_take_courses(request):
    if request.method == 'GET':
        year = request.GET.get('year', '2005-2006')
        sem = request.GET.get('sem', 1)

        user = request.user
        
        takes = Takes.objects.filter(student__user__exact=user,
                course__academic_year__exact=year,
                course__semester__exact=sem)

        courseArr = []
        for take in takes:
            courseObj = {}
            courseObj['name'] = take.course.name
            courseObj['academic_year'] = take.course.academic_year
            courseObj['semester'] = take.course.semester
            courseObj['from_week'] = take.course.from_week
            courseObj['to_week'] = take.course.to_week
            courseObj['course_time'] = take.course.course_time
            courseObj['teacher'] = take.course.teacher.teacher_name
            courseObj['credit'] = take.course.credit
            courseObj['location'] = take.course.location
            courseObj['capacity'] = take.course.capacity
            courseObj['exam_method'] = take.course.exam_method
            courseObj['course_type'] = take.courseTypeToUnicode[course.course_type.type_name]
            courseObj['department'] = take.course.department.name
            
            courseArr.append(courseObj)

        retJson = {'courses': courseArr, 
                'studentid': request.user.username
                }
        return HttpResponse(simplejson.dumps(retJson),
                mimetype='application/json')
    else:
        return HttpResponseBadRequest('Invalid Method')
            
