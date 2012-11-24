# -*- coding:utf-8 -*-

from EduAdminSystem import settings
from django.core.management import setup_environ
setup_environ(settings)
from django.contrib.auth.models import User
from school.models import *
from student.models import Student, StudentMeta
from teacher.models import Teacher

students = [
        {
            'username': '10383001',
            'password': '123456',
            'student_name': 'ABC'
        },
        {
            'username': '10383002',
            'password': '123456',
            'student_name': 'BCD'
        }
    ]

teachers = [
        {
            'username': 'jqg',
            'password': 'jqg',
            'teacher_name': '纪庆革',
            'title': 'P'
        }    
    ]

sist = School.objects.get_or_create(name='SIST')[0]
sist.save()
cs = Department.objects.get_or_create(name='CS', school=sist)[0]
cs.save()
cst = Speciality.objects.get_or_create(name='CST', department=cs)[0]
cst.save()

stuMeta = StudentMeta.objects.get_or_create(type_name='UG', year='2010',
        major=cst)[0]

for student in students:
    user = User.objects.get_or_create(username=student['username'])[0]
    user.set_password(student['password'])
    user.save()
    stud = Student.objects.get_or_create(student_name=student['student_name'],
            student_meta=stuMeta, user=user)[0]
    stud.save()

for teacher in teachers:
    user = User.objects.get_or_create(username=teacher['username'])[0]
    user.set_password(teacher['password'])
    user.save()
    teac = Teacher.objects.get_or_create(teacher_name=teacher['teacher_name'],
            department=cs, user=user, title=teacher['title'])[0]
    teac.save()
    
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
