# -*- coding:utf-8 -*-

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from course.models import CourseType, Course
from student.models import Student
from django.utils import simplejson

coursetype = {
        'po': CourseType.PUB_ELECTIVE, 
        'pr': CourseType.PUB_COURSE,
        'mo': CourseType.PRO_ELECTIVE,
        'mr': CourseType.PRO_COURSE
        }

@login_required
def get_available_list(request):
    if request.method == 'GET':
        cultivate = request.GET.get('cultivate', 0)
        ct = coursetype[request.GET.get('course-type-1', 'po')]
        academic_year = request.GET.get('academic_year', '2005-2006')
        sem = request.GET.get('sem', 1)
        
        courseType = CourseType.objects.get(type_name=ct)
        student = Student.objects.get(user=request.user)
        # it only work for major now.
        if cultivate == 0:
            department = student.student_meta.major.department
        
        courses = Course.objects.filter(academic_year=academic_year,
                semester=sem, course_type=courseType,
                department=department)
        
        courseArr = []
        for course in courses:
            courseObj = {}
            courseObj['name'] = course.name
            courseObj['academic_year'] = course.academic_year
            courseObj['semester'] = course.semester
            courseObj['from_week'] = course.from_week
            courseObj['to_week'] = course.to_week
            courseObj['course_time'] = course.course_time
            courseObj['teacher'] = course.teacher.teacher_name
            courseObj['credit'] = course.credit
            courseObj['location'] = course.location
            courseObj['capacity'] = course.capacity
            courseObj['exam_method'] = course.exam_method
            courseObj['course_type'] =\
                CourseType.get_coursetype(course.course_type)
            courseObj['department'] = course.department.name
            
            courseArr.append(courseObj)

        retJson = {'courses': courseArr, 
                'studentid': request.user.username
                }
        
        return HttpResponse(simplejson.dumps(retJson),
                mimetype='application/json')
    else:
        return HttpResponseBadRequest('Invalid Method')
