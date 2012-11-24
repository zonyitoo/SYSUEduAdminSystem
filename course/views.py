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

courseTypeToUnicode = {
            CourseType.PUB.COURSE: u'公共必修课',
            CourseType.PUB_ELECTIVE: u'公共选修课', 
            CourseType.PRO_COURSE: u'专业必修课',
            CourseType.PRO_ELECTIVE: u'专业选修课'
        }

@login_required
def get_available_list(request):
    if request.method == 'GET':
        caltivate = request.GET.get('cultivate', 0)
        ct = coursetype[request.GET.get('course-type-1', 'po')]
        academic_year = request.GET.get('academic_year', '2005-2006')
        sem = request.GET.get('sem', 1)
        
        courseType = CourseType.objects.get(type_name=ct)
        student = Student.objects.get(user=request.user)
        # it only work for major now.
        if caltivate == 0:
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
                courseTypeToUnicode[course.course_type.type_name]
            courseObj['department'] = course.department.name
            
            courseArr.append(courseObj)

        retJson = {'courses': courseArr, 
                'studentid': request.user.username
                }
        
        return HttpResponse(simplejson.dumps(retJson),
                mimetype='application/json')
    else:
        return HttpResponseBadRequest('Invalid Method')
