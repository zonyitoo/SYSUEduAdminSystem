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
            courseObj['place'] = [{'place': loc.location}
                    for loc in course.location.all()]
            courseObj['capacity'] = course.capacity
            courseObj['hastaken'] =\
                Takes.objects.filter(course=course).count()
            courseObj['exam_method'] = course.exam_method
            courseObj['course_type'] = course.course_type.get_coursetype()
            courseObj['department'] = course.department.name

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
