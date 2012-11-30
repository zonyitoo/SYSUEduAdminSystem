from django.http import HttpResponseForbidden, HttpResponseBadRequest
from ajaxutils.decorators import ajax

from coures.models import Course, CourseType
from teacher.models import Teacher
from take.models import Takes

convertCourseType = {
            
        }

@ajax(login_required=True, require_GET=True)
def get_avaliable_courses(request):
    if hasattr(request.user, 'teacher'):
        teacher = Teacher.objects.get(user=request.user)
    else:
        return HttpResponseForbidden("Only teacher can access")

    year = request.GET['year']
    course_type = convertCourseType[request.GET['course_type']]

    course_type = CourseType.objects.get(type_name=course_type) 

    courses = Course.objects.filter(year=year, course_type=course_type)
    for course in courses:
        courseObj = {}
        courseObj['id'] = course.id
        courseObj['name'] = course.name
        courseObj['academic_year'] = course.academic_year
        courseObj['semester'] = course.semester
        courseObj['from_week'] = course.from_week
        courseObj['to_week'] = course.to_week
        courseObj['course_time'] = [
                {
                    'week': t.week, 
                    'time': t.time,
                    'place': t.location
                }
                for t in course.course_time.all()]
        courseObj['credit'] = course.credit
        courseObj['capacity'] = course.capacity
        courseObj['hastaken'] =\
            Takes.objects.filter(course=course).count()
        courseObj['exam_method'] = course.exam_method
        courseObj['course_type'] = course.course_type.get_coursetype()
        courseObj['department'] = course.department.name

@ajax(login_required=True, require_GET=True)
def get_student_list(request):
    if hasattr(request.user, 'teacher'):
        teacher = Teacher.objects.get(user=request.user)
    else:
        return HttpResponseForbidden("Only teacher can access")

    course_id = int(request.GET['course_id'])
    year = request.GET['year']

    takes = Takes.objects.filter(
                course = Course.objects.get(id=course_id),
                year = year,
                teacher = teacher
            )

    for take in takes:
        pass

