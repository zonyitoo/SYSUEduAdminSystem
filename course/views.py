# -*- coding:utf-8 -*-

from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required

from course.models import CourseType, Course
from take.models import Takes
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
        cultivate = int(request.GET.get('cultivate', 0))
        ct = []
        if request.GET['po'] == 'true':
            ct.append(coursetype['po'])
        if request.GET['pr'] == 'true':
            ct.append(coursetype['pr'])
        if request.GET['mo'] == 'true':
            ct.append(coursetype['mo'])
        if request.GET['mr'] == 'true':
            ct.append(coursetype['mr'])
        academic_year = request.GET.get('academic_year', '2012-2013')
        sem = request.GET.get('sem', 1)
        
        courseType = []
        for cot in ct:
            ctobj = CourseType.objects.get(type_name=cot)
            courseType.append(ctobj)

        student = Student.objects.get(user=request.user)
        # it only work for major now.
        department = None
        if cultivate == 0:
            department = student.student_meta.major.department
        
        courseArr = []
        for ict in courseType:
            courses = Course.objects.filter(academic_year=academic_year,
                    semester=sem, course_type=ict,
                    department=department)

            for course in courses:
                courseObj = {}
                courseObj['id'] = course.id
                courseObj['name'] = course.name
                courseObj['academic_year'] = course.academic_year
                courseObj['semester'] = course.semester
                courseObj['from_week'] = course.from_week
                courseObj['to_week'] = course.to_week
                courseObj['course_time'] = [{'week': t.week, 'time': t.time}
                        for t in course.course_time.all()]
                courseObj['teacher'] = {
                            'teacher_name': course.teacher.teacher_name,
                            'title': course.teacher.get_title_unicode(),
                            'img_addr': course.teacher.img_addr,
                            'site': course.teacher.site,
                            'department': course.teacher.department.name
                        }
                courseObj['credit'] = course.credit
                courseObj['location'] = course.location
                courseObj['capacity'] = course.capacity
                courseObj['exam_method'] = course.exam_method
                courseObj['course_type'] = course.course_type.get_coursetype()
                courseObj['department'] = course.department.name

                try:
                    Takes.objects.get(course=course, student=student)
                    courseObj['take'] = True
                except:
                    courseObj['take'] = False
                
                courseArr.append(courseObj)

        retJson = {'courses': courseArr, 
                'studentid': request.user.username
                }
        
        return HttpResponse(simplejson.dumps(retJson),
                mimetype='application/json')
    else:
        return HttpResponseBadRequest('Invalid Method')
