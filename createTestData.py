#!/usr/bin/env python
# -*- coding:utf-8 -*-

from EduAdminSystem import settings
from django.core.management import setup_environ
setup_environ(settings)
from django.contrib.auth.models import User, Group, Permission

"""
    This script just for generating test data.
    If you get runtime errors, you can
        1. Drop eduadminsystemdb database and recreate it
        2. Debug this script

    Thie script will delete all your remain data
"""

## Schools
from school.models import School, Department, Speciality

schools = [
    {
        'name': 'SIST'
        },
    {
        'name': 'SS'
        }
]

School.objects.all().delete()
for s in schools:
    obj = School.objects.get_or_create(**s)
    if not obj[1]:
        print 'School', s['name'], 'exists'
    else:
        print 'Creating School', s['name']
        obj[0].save()

departments = [
    {
        'name': 'CS',
        'school': School.objects.get(name='SIST')
        }        
]

Department.objects.all().delete()
for d in departments:
    obj = Department.objects.get_or_create(**d)
    if not obj[1]:
        print 'Department', d['name'], 'exists'
    else:
        print 'Creating Department', d['name']
        obj[0].save()



specialities = [
    {
        'name': 'CST',
        'department': Department.objects.get(name='CS')
        }        
]

Speciality.objects.all().delete()
for s in specialities:
    obj = Speciality.objects.get_or_create(**s)
    if not obj[1]:
        print 'Speciality', s['name'], 'exists'
    else:
        print 'Creating Speciality', s['name']
        obj[0].save()


# Students
from student.models import Student, StudentMeta

studentMetas = [
    {
        'type_name': StudentMeta.UNGRADUATED,
        'year': '2010',
        'major': Speciality.objects.get(name='CST')
    }        
]

StudentMeta.objects.all().delete()
for sm in studentMetas:
    obj = StudentMeta.objects.get_or_create(**sm)
    if not obj[1]:
        print 'StudentMeta', sm, 'exists'
    else:
        print 'Creating StudentMeta', sm
        obj[0].save()

students = [
    {
    "user": {
        "username": "10383001",
        "password": "123456"
    },
    "student": {
        "student_name": "ABC",
        "student_meta": StudentMeta.objects.get(
            major=Speciality.objects.get(name='CST'), year=2010)
        }
    },
    {
    "user": {
        "username": "10383002",
        "password": "123456",
        },
    "student": {
        "student_name": "BCD",
        "student_meta": StudentMeta.objects.get(
            major=Speciality.objects.get(name='CST'), year=2010)
        }
    },
    {
    "user": {
        "username": "10383067",
        "password": "zonyitoo",
        },
    "student": {
        "student_name": "钟宇腾",
        "student_meta": StudentMeta.objects.get(
             major=Speciality.objects.get(name='CST'), year=2010)
        }
    }
]

studentGroup = Group.objects.get_or_create(name='student')
if not studentGroup[1]:
    permaddtake = Permission.objects.get(codename='add_takes')
    permdeltake = Permission.objects.get(codename='delete_takes')
    studentGroup[0].permissions = [permaddtake, permdeltake]
Student.objects.all().delete()
for student in students:
    try:
        user = User.objects.get(username=student['user']['username'])
    except User.DoesNotExist:
        user = User.objects.create_user(**student['user'])
        user.groups = [studentGroup[0]]
        user.save()

    obj = Student.objects.get_or_create(user=user, **student['student'])
    if not obj[1]:
        print 'Student', obj[0].student_name, 'exists'
    else:
        print 'Creating Student', obj[0].student_name
        obj[0].save()

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
                'title': Teacher.TITLE[1][0],
                'department': Department.objects.get(name='CS')
                }
            },
        {
            'user': {
                'username': 'yy',
                'password': 'yy',
                },
            'teacher': {
                'teacher_name': '衣扬',
                'title': Teacher.TITLE[1][0],
                'department': Department.objects.get(name='CS')
                }
            },
        {
            'user': {
                'username': 'qdw',
                'password': 'qdw',
                },
            'teacher': {
                'teacher_name': '邱道文',
                'title': Teacher.TITLE[2][0],
                'department': Department.objects.get(name='CS')
                }
            },
        {
            'user': {
                'username': 'naive',
                'password': 'naive',
                },
            'teacher': {
                'teacher_name': '拿衣服',
                'title': Teacher.TITLE[2][0],
                'department': Department.objects.get(name='CS')
                }
            }
    ]

teacherGroup = Group.objects.get_or_create(name='teacher')
if not teacherGroup[1]:
    teacherGroup[0].permissions = []
Teacher.objects.all().delete()
for teacher in teachers:
    try:
        user = User.objects.get(username=teacher['user']['username'])
    except User.DoesNotExist:
        user = User.objects.create_user(**teacher['user'])
        user.groups = [teacherGroup[0]]
        user.save()
    teac = Teacher.objects.get_or_create(user=user, **teacher['teacher'])
    if not teac[1]:
        print 'Teacher', teac[0].teacher_name, 'exists'
    else:
        print 'Creating Teacher', teac[0].teacher_name
        teac[0].save()
    
## Courses
from course.models import CourseType, Course, CourseTime
for t in CourseType.COURSE_TYPE:
    CourseType.objects.get_or_create(type_name=t[0])[0].save()

courses = [
        {
            'time': [
                {
                    'week': 2,
                    'time': 'DE',
                    'location': '东C501'
                    }
                ],
            'course': {
                'name': '计算机图形学',
                'academic_year': '2012-2013',
                'semester': 1,
                'from_week': 1,
                'to_week': 20,
                'teacher': Teacher.objects.get(teacher_name='纪庆革'),
                'credit': 2,
                'capacity': 9999,
                'hastaken': 1,
                'exam_method': '考查',
                'course_type':
                    CourseType.objects.get(type_name=CourseType.COURSE_TYPE[3][0]),
                'department': Department.objects.get(name='CS')
                }
            },
        {
            'time': [
                {
                    'week': 2,
                    'time': 'DE',
                    'location': '东C501'
                    }
                ],
            'course': {
                'name': '计算机图形学',
                'academic_year': '2011-2012',
                'semester': 1,
                'from_week': 1,
                'to_week': 20,
                'teacher': Teacher.objects.get(teacher_name='纪庆革'),
                'credit': 2,
                'capacity': 9999,
                'exam_method': '考查',
                'course_type':
                    CourseType.objects.get(type_name=CourseType.COURSE_TYPE[3][0]),
                'department': Department.objects.get(name='CS')
                }
            },
        {
            'time': [
                {
                    'week': 3,
                    'time': 'GHI',
                    'location': '东A302'
                    }
                ],
            'course': {
                'name': '软件工程导论及实践',
                'academic_year': '2012-2013',
                'semester': 1,
                'from_week': 1,
                'to_week': 20,
                'teacher': Teacher.objects.get(teacher_name='衣扬'),
                'credit': 3,
                'capacity': 9999,
                'exam_method': '考查',
                'course_type':
                    CourseType.objects.get(type_name=CourseType.COURSE_TYPE[3][0]),
                'department': Department.objects.get(name='CS')
                }
            },
        {
            'time': [
                {
                    'week': 2,
                    'time': 'ABC',
                    'location': '东B202'
                    }
                ],
            'course': {
                'name': '数学分析II',
                'academic_year': '2010-2011',
                'semester': 2,
                'from_week': 1,
                'to_week': 18,
                'teacher': Teacher.objects.get(teacher_name='邱道文'),
                'final_percentage': 70,
                'credit': 3,
                'capacity': 9999,
                'hastaken': 1,
                'exam_method': '笔试',
                'course_type':
                    CourseType.objects.get(type_name=CourseType.COURSE_TYPE[2][0]),
                'department': Department.objects.get(name='CS')
                }
            },
        {
            'time': [
                {
                    'week': 2,
                    'time': 'CDE',
                    'location': '东C201'
                    }
                ],
            'course': {
                'name': 'Test_Collision1',
                'academic_year': '2012-2013',
                'semester': 1,
                'from_week': 1,
                'to_week': 18,
                'teacher': Teacher.objects.get(teacher_name='拿衣服'),
                'credit': 3,
                'capacity': 9999,
                'hastaken': 1,
                'exam_method': '笔试',
                'course_type':
                    CourseType.objects.get(type_name=CourseType.COURSE_TYPE[3][0]),
                'department': Department.objects.get(name='CS')
                }
            },
        {
            'time': [
                {
                    'week': 3,
                    'time': 'GH',
                    'location': '东C201'
                    }
                ],
            'course': {
                'name': 'Test_Capacity1',
                'academic_year': '2012-2013',
                'semester': 1,
                'from_week': 1,
                'to_week': 18,
                'teacher': Teacher.objects.get(teacher_name='拿衣服'),
                'credit': 2,
                'capacity': 5,
                'hastaken': 5,
                'exam_method': '笔试',
                'course_type':
                    CourseType.objects.get(type_name=CourseType.COURSE_TYPE[1][0]),
                'department': Department.objects.get(name='CS')
                }
            }
    ]

Course.objects.all().delete()
for c in courses:
    obj = Course.objects.get_or_create(**c['course'])
    if not obj[1]:
        print "Course", obj[0].name, 'exists'
    else:
        print "Creating Course", obj[0].name
        obj[0].course_time = [CourseTime.objects.get_or_create(**ti)[0] 
                for ti in c['time']]
        obj[0].save()

## Takes
from take.models import Takes
takes = [
            {
                'course': Course.objects.get(name='计算机图形学',
                    academic_year='2012-2013'),
                'student': Student.objects.get(student_name='ABC')
            },
            {
                'course': Course.objects.get(name='计算机图形学',
                    academic_year='2012-2013'),
                'student': Student.objects.get(student_name='钟宇腾')
            },
            {
                'course': Course.objects.get(name='数学分析II'),
                'student': Student.objects.get(student_name='钟宇腾'),
                'usual_score': 80.0,
                'final_score': 60.0,
                'score': 60.0 * 0.7 + 80.0 * 0.3,
                'rank': 2,
                'has_assessment': True,
                'screened': True
            },
            {
                'course': Course.objects.get(name='数学分析II'),
                'student': Student.objects.get(student_name='ABC'),
                'usual_score': 90.0,
                'final_score': 95.0,
                'score': 95.0 * 0.7 + 90.0 * 0.3,
                'rank': 1,
                'has_assessment': True,
                'screened': True
            }
    ]

Takes.objects.all().delete()
for t in takes:
    obj = Takes.objects.get_or_create(**t)
    if not obj[1]:
        print "Take", t, "exists"
    else:
        print "Creating Take", t
        obj[0].course.hastaken += 1
        obj[0].course.save()
        obj[0].save()
