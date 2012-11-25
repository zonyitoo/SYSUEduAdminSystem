# -*- coding:utf-8 -*-
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from take.models import Takes
from student.models import Student
from course.models import Course, CourseType
from django.utils import simplejson

@login_required
def get_take_courses(request):
    if request.method == 'GET':
        year = request.GET.get('year', '2012-2013')
        sem = request.GET.get('sem', 1)

        user = request.user
        
        takes = Takes.objects.filter(student__user__exact=user,
                course__academic_year__exact=year,
                course__semester__exact=sem)
           
        courseArr = []
        for take in takes:
            courseObj = {}
            courseObj['id'] = take.course.id
            courseObj['name'] = take.course.name
            courseObj['academic_year'] = take.course.academic_year
            courseObj['semester'] = take.course.semester
            courseObj['from_week'] = take.course.from_week
            courseObj['to_week'] = take.course.to_week
            courseObj['course_time'] = [{'week': t.week, 'time': t.time}
                    for t in take.course.course_time.all()]
            courseObj['teacher'] = {
                        'teacher_name': take.course.teacher.teacher_name,
                        'title': take.course.teacher.get_title_unicode(),
                        'img_addr': take.course.teacher.img_addr,
                        'site': take.course.teacher.site,
                        'department': take.course.teacher.department.name
                    }
            courseObj['credit'] = take.course.credit
            courseObj['location'] = take.course.location
            courseObj['capacity'] = take.course.capacity
            courseObj['exam_method'] = take.course.exam_method
            courseObj['course_type'] = CourseType.get_coursetype(take.course.course_type)

            courseArr.append(courseObj)

        retJson = {'courses': courseArr, 
                'studentid': request.user.username
                }
        return HttpResponse(simplejson.dumps(retJson),
                mimetype='application/json')
    else:
        return HttpResponseBadRequest('Invalid Method')

@login_required
def get_take_plan(request):
    if request.method == 'GET':
        cultivate = int(request.GET.get('cultivate', 0))
        
        # only work for student 
        user = request.user
        student = Student.objects.get(user = user)
        
        # only work for major
        department = None
        if cultivate == 0:
            department = student.student_meta.major.department

        takes = Takes.objects.filter(student__user__exact = user,
                course__department__exact = department)
            
        courseArr = []
        for take in takes:
            courseObj = {}
            courseObj['id'] = take.course.id
            courseObj['name'] = take.course.name
            courseObj['academic_year'] = take.course.academic_year
            courseObj['semester'] = take.course.semester
            courseObj['from_week'] = take.course.from_week
            courseObj['to_week'] = take.course.to_week
            courseObj['course_time'] = [{'week': t.week, 'time': t.time}
                    for t in take.course.course_time.all()]
            courseObj['teacher'] = {
                        'teacher_name': take.course.teacher.teacher_name,
                        'title': take.course.teacher.get_title_unicode(),
                        'img_addr': take.course.teacher.img_addr,
                        'site': take.course.teacher.site,
                        'department': take.course.teacher.department.name
                    }
            courseObj['credit'] = take.course.credit
            courseObj['location'] = take.course.location
            courseObj['capacity'] = take.course.capacity
            courseObj['exam_method'] = take.course.exam_method
            courseObj['course_type'] = CourseType.get_coursetype(take.course.course_type)
            courseObj['department'] = take.course.department.name
            
            courseArr.append(courseObj)

        retJson = {'courses': courseArr, 
                'studentid': request.user.username
                }
        return HttpResponse(simplejson.dumps(retJson),
                mimetype='application/json')
    else:
        return HttpResponseBadRequest('Invalid Method')
