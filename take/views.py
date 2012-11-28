# -*- coding:utf-8 -*-
from ajaxutils.decorators import ajax
from take.models import Takes
from student.models import Student
from course.models import CourseType

@ajax(login_required=True, require_GET=True)
def get_take_courses(request):
    year = request.GET.get('school-year', '')
    sem = request.GET.get('school-term', '')

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
        courseObj['course_time'] = [
                {
                    'week': t.week, 
                    'time': t.time,
                    'place': t.location
                }
                for t in take.course.course_time.all()]
        courseObj['teacher'] = {
                    'teacher_name': take.course.teacher.teacher_name,
                    'title': take.course.teacher.get_title_unicode(),
                    'img_addr': take.course.teacher.img_addr,
                    'site': take.course.teacher.site,
                    'department': take.course.teacher.department.name
                }
        courseObj['credit'] = take.course.credit
        courseObj['capacity'] = take.course.capacity
        courseObj['exam_method'] = take.course.exam_method
        courseObj['course_type'] = CourseType.get_coursetype(take.course.course_type)

        courseArr.append(courseObj)

    return {
        'courses': courseArr, 
        'studentid': request.user.username
    }

@ajax(login_required=True, require_GET=True)
def get_take_score(request):
    year = request.GET.get('school-year', '')
    sem = request.GET.get('school-term', '')

    user = request.user
    
    takes = Takes.objects.filter(student__user__exact=user,
            course__academic_year__exact=year,
            course__semester__exact=sem, has_assessment=True)
       
    courseArr = []
    for take in takes:
        courseObj = {}
        courseObj['id'] = take.course.id
        courseObj['name'] = take.course.name
        courseObj['academic_year'] = take.course.academic_year
        courseObj['semester'] = take.course.semester
        courseObj['teacher'] = {
                    'teacher_name': take.course.teacher.teacher_name,
                    'title': take.course.teacher.get_title_unicode(),
                    'img_addr': take.course.teacher.img_addr,
                    'site': take.course.teacher.site,
                    'department': take.course.teacher.department.name
                }
        courseObj['credit'] = take.course.credit
        courseObj['course_type'] = CourseType.get_coursetype(take.course.course_type)
        courseObj['usual_score'] = take.usual_score
        courseObj['final_score'] = take.final_score
        courseObj['final_percentage'] = take.final_percentage

        courseArr.append(courseObj)

    return {
        'courses': courseArr, 
        'studentid': request.user.username
    }
