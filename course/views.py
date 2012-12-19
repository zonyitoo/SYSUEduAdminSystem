# -*- coding:utf-8 -*-

from django.http import HttpResponseForbidden, HttpResponseBadRequest
from course.models import Course
from take.models import Takes
from student.models import Student
from ajaxutils.decorators import ajax
from django.db.models import Avg
import time

COURSE_TYPE = [
    Course.PUB_ELECTIVE, 
    Course.PUB_COURSE,
    Course.PRO_ELECTIVE,
    Course.PRO_COURSE,
    Course.GYM_ELECTIVE,
]

@ajax(login_required=True, require_GET=True)
def get_available_list(request):
    try:
        cultivate = int(request.GET.get('cultivate', ''))
    
        course_type = COURSE_TYPE[int(request.GET['course_type'])]
    except:
        return HttpResponseBadRequest('Invalid Arguments')
    
    t = time.localtime(time.time())
    year = t.tm_year
    month = t.tm_mon
    if month >= 9 or month <= 1:
        year = str(year) + '-' + str(year + 1)
    else:
        year = str(year - 1) + '-' + str(year)

    if month >= 9 or month <= 1:
        sem = 1
    elif month > 1 and month <= 6:
        sem = 2
    else:
        sem = 3

    print year, sem

    student = Student.objects.get(user=request.user)
    # it only work for major now.
    if cultivate == 0:
        stud_class = student.student_meta.major

    courseArr = []
    if request.GET['course_type'] == '0':
        courses = Course.objects.filter(academic_year=year,
                semester=sem,
                course_type=course_type).order_by('teacher__teacher_name')
    elif request.GET['course_type'] == '1':
        courses = Course.objects.filter(academic_year=year,
                semester=sem, course_type=course_type,
                department=stud_class.speciality.department).order_by('teacher__teacher_name')
    elif request.GET['course_type'] == '4':
        courses = Course.objects.filter(academic_year=year,
                semester=sem, course_type=course_type).order_by('teacher__teacher_name')
    else:
        courses = Course.objects.filter(academic_year=year,
                semester=sem, course_type=course_type,
                class_oriented=stud_class).order_by('teacher__teacher_name')

    for course in courses:
        courseObj = course.getDataDict()

        try:
            t = Takes.objects.get(course=course, student=student)
            #if course.screened:
            if t.screened:
                courseObj['take'] = 1
                #else: courseObj['take'] = 2
            else:
                courseObj['take'] = 3
        except:
            courseObj['take'] = 0 # The Student has not take this course
        
        courseArr.append(courseObj)

    return {
        'courses': courseArr, 
    }

@ajax(login_required=True, require_GET=True)
def get_educate_plan(request):
    try:
        cultivate = int(request.GET.get('cultivate', ''))
    except:
        return HttpResponseBadRequest('Invalid Arguments')
    
    # only work for student 
    user = request.user
    student = Student.objects.get(user = user)
    
    # only work for major
    stud_class = None
    if cultivate == 0:
        stud_class = student.student_meta.major
    
    student_timelife = []
    curyear = int(student.student_meta.year)
    for i in range(0, 3):
        student_timelife.append(str(curyear) + '-' + str(curyear + 1))
        curyear += 1

    courses = Course.objects.filter(academic_year__in=student_timelife,
            class_oriented=stud_class).order_by("academic_year")
    
    return {
        'student': student.getDataDict(),
        'courses': [course.getDataDict() for course in courses],
    }
    
@ajax(login_required=True, require_GET=True)
def get_course_statistic(request):
    if hasattr(request.user, 'student'):
        return HttpResponseForbidden(
            'Student is not allowed to assess the statistic')

    try:
        course_id = request.GET['course_id']
    except:
        return HttpResponseBadRequest('Invalid Arguments')

    try:
        course = Course.objects.get(id=int(course_id))
    except Course.DoesNotExist:
        return HttpResponseBadRequest('Course does not exist')

    takes = Takes.objects.filter(course=course)

    avg_score = takes.aggregate(Avg('score')).values()[0]
    pass_cnt = takes.filter(score__gte=60)
    notpass_cnt = takes.count() - pass_cnt

    return {
        'avg_score': avg_score,
        'pass_cnt': pass_cnt,
        'notpass_cnt': notpass_cnt,
        'course': course.getDataDict(),
    }
    
