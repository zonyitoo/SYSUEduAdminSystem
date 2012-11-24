# -*- coding:utf-8 -*-

from EduAdminSystem import settings
from django.core.management import setup_environ
setup_environ(settings)
from django.contrib.auth.models import User

## Schools
from school.models import School, Department, Speciality

sist = School.objects.get_or_create(name='SIST')[0]
sist.save()
cs = Department.objects.get_or_create(name='CS', school=sist)[0]
cs.save()
cst = Speciality.objects.get_or_create(name='CST', department=cs)[0]
cst.save()

# Students
from student.models import Student, StudentMeta

stuMeta = StudentMeta.objects.get_or_create(type_name='UG', year='2010',
        major=cst)[0]

students = [
        {
            'user': {
                    'username': '10383001',
                    'password': '123456'
                },
            'student': {
                'student_name': 'ABC',
                'student_meta': StudentMeta.objects.get(year=2010)
                }
            },
        {
            'user': {
                'username': '10383002',
                'password': '123456',
                },
            'student': {
                'student_name': 'BCD',
                'student_meta': StudentMeta.objects.get(year=2010)
                }
            },
        {
            'user': {
                'username': '10383067',
                'password': 'zonyitoo',
                },
            'student': {
                'student_name': '钟宇腾',
                'student_meta': StudentMeta.objects.get(year=2010)
                }
            }
        ]

for student in students:
    user = User.objects.get_or_create(**student['user'])[0]
    user.save()
    stud = Student.objects.get_or_create(user=user, **student['student'])[0]
    stud.save()

## Teachers
from teacher.models import Teacher
teachers = [
        {
            'user': {
                'username': 'jqg',
                'password': 'jqg',
                },
            'teacher': {
                'teacher_name': '纪庆革',
                'title': Teacher.TITLE[2][0],
                'department': Department.objects.get(name='CS')
                }
            }    
        ]

for teacher in teachers:
    user = User.objects.get_or_create(**teacher['user'])[0]
    user.save()
    teac = Teacher.objects.get_or_create(user=user, **teacher['teacher'])[0]
    teac.save()
    
## Courses
from course.models import CourseType, Course
for t in CourseType.COURSE_TYPE:
    CourseType.objects.get_or_create(type_name=t[0])[0].save()

courses = [
        {
            'name': '计算机图形学',
            'academic_year': '2012-2013',
            'semester': Course.SEMESTER[0][0],
            'from_week': 1,
            'to_week': 20,
            'course_time': 'DE',
            'teacher': Teacher.objects.get(teacher_name='纪庆革'),
            'credit': 2,
            'location': 'addr',
            'capacity': 9999,
            'exam_method': '考查',
            'course_type':
                CourseType.objects.get(type_name=CourseType.COURSE_TYPE[0][0]),
            'department': cs
            } 
    ]

for c in courses:
    Course.objects.get_or_create(**c)[0].save()
