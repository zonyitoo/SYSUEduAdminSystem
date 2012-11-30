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
        
    plan = {}
    plan['pr_req'] = student.student_meta.req_pubcourse
    plan['po_req'] = student.student_meta.req_pubelective
    plan['mr_req'] = student.student_meta.req_procourse
    plan['mo_req'] = student.student_meta.req_proelective
    plan['pr_credit'] = student.pubcourse_credit
    plan['po_credit'] = student.pubelective_credit
    plan['mr_credit'] = student.procourse_credit
    plan['mo_credit'] = student.proelective_credit
    plan['pr_gpa'] = str(student.pubcourse_gpa)
    plan['po_gpa'] = str(student.pubelective_gpa)
    plan['mr_gpa'] = str(student.procourse_gpa)
    plan['mo_gpa'] = str(student.proelective_gpa)
    plan['gpa'] = str(student.gpa)
    plan['pubcourse_gpa'] = str(student.pubcourse_gpa)
    plan['pubelective_gpa'] = str(student.pubelective_gpa)
    plan['procourse_gpa'] = str(student.procourse_gpa)
    plan['proelective_gpa'] = str(student.proelective_gpa)
    plan['student_type'] = student.student_meta.type_name
    plan['year'] = int(student.student_meta.year)

    grade={}
    grade['fresh'] = str(plan['year']) + '-' + str(plan['year'] + 1)
    grade['sophomore'] = str(plan['year'] + 1) + '-' + str(plan['year'] + 2)
    grade['junior'] = str(plan['year'] + 2) + '-' + str(plan['year'] + 3)
    grade['senior'] = str(plan['year'] + 3) + '-' + str(plan['year'] + 4)

    courses = Course.objects.filter(academic_year__in=[grade['fresh'],grade['sophomore'],grade['junior'],grade['senior']],
            department=department)

    courseArr = [course.getDataDict() for course in courses]
    
    return {
        'plan': plan, 
        'courses': courseArr,
        'studentid': request.user.username
        }
