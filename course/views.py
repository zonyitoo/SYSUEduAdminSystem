# -*- coding:utf-8 -*-

from course.models import CourseType, Course
from take.models import Takes
from student.models import Student
from ajaxutils.decorators import ajax
import time

COURSE_TYPE = {
    CourseType.PUB_ELECTIVE, 
    CourseType.PUB_COURSE,
    CourseType.PRO_ELECTIVE,
    CourseType.PRO_COURSE
}

@ajax(login_required=True, require_GET=True)
def get_available_list(request):
    cultivate = int(request.GET.get('cultivate', ''))
    
    course_type = COURSE_TYPE[int(request.GET['course_type'])]
    
    t = time.localtime(time.time())
    year = t.tm_year
    month = t.tm_mon
    if month >= 9 or month <= 1:
        year = str(year) + '-' + str(year + 1)
    else:
        year = str(year - 1) + '-' + str(year)

    if month >= 9 and month <= 1:
        sem = 1
    elif month > 1 and month <= 6:
        sem = 2
    else:
        sem = 3

    student = Student.objects.get(user=request.user)
    # it only work for major now.
    if cultivate == 0:
        stud_class = student.student_meta.major

    courseArr = []
    if request.GET['course_type'] == '0':
        courses = Course.objects.filter(academic_year=year,
                semester=sem, course_type=course_type)
    elif request.GET['course_type'] == '1':
        courses = Course.objects.filter(academic_year=year,
                semester=sem, course_type=course_type,
                department=stud_class.speciality.department)
    else:
        courses = Course.objects.filter(academic_year=year,
                semester=sem, course_type=course_type,
                class_oriented=stud_class)

    for course in courses:
        courseObj = course.getDataDict()

        try:
            t = Takes.objects.get(course=course, student=student)
            if course.screened:
                if t.screened: courseObj['take'] = 1
                else: courseObj['take'] = 2
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
    cultivate = int(request.GET.get('cultivate', ''))
    
    # only work for student 
    user = request.user
    student = Student.objects.get(user = user)
    
    # only work for major
    department = None
    if cultivate == 0:
        department = student.student_meta.major.department
    
    student_timelife = []
    curyear = int(student.student_meta.year)
    for i in range(0, 3):
        student_timelife.append(str(curyear) + '-' + str(curyear + 1))
        curyear += 1

    courses = Course.objects.filter(academic_year__in=student_timelife,
            department=department).order_by("academic_year")
    
    return {
        'student': student.getDataDict(),
        'courses': [course.getDataDict() for course in courses],
    }
