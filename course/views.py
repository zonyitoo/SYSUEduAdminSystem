# -*- coding:utf-8 -*-

from course.models import CourseType, Course
from take.models import Takes
from student.models import Student
from ajaxutils.decorators import ajax

coursetype = {
        'po': CourseType.PUB_ELECTIVE, 
        'pr': CourseType.PUB_COURSE,
        'mo': CourseType.PRO_ELECTIVE,
        'mr': CourseType.PRO_COURSE
        }

@ajax(login_required=True, require_GET=True)
def get_available_list(request):
    cultivate = int(request.GET.get('cultivate', ''))
    ct = []
    if request.GET['po'] == 'true':
        ct.append(coursetype['po'])
    if request.GET['pr'] == 'true':
        ct.append(coursetype['pr'])
    if request.GET['mo'] == 'true':
        ct.append(coursetype['mo'])
    if request.GET['mr'] == 'true':
        ct.append(coursetype['mr'])
    academic_year = request.GET.get('school-year', '')
    sem = request.GET.get('school-term', '')
    
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
        'studentid': request.user.username
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
