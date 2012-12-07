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
        },
    {
	'name': 'LAW'
	},
    {
	'name': 'LIFESCI'
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
        },
    {
	'name': 'SE',
	'school': School.objects.get(name='SS')
	},
    {
	'name': 'LAW',
	'school': School.objects.get(name='LAW')
	},
    {
	'name': 'BIO',
	'school': School.objects.get(name='LIFESCI')
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
            },
	{
	    'user': {
		'username': 'lwj',
		'password': 'lwj',
		},
	    'teacher': {
		'teacher_name': '李文军',
		'title': Teacher.TITLE[2][0],
		'department': Department.objects.get(name='SE')
		}
	    },
	{
	    'user': {
		'username': 'dl',
		'password': 'dl',
		},
	    'teacher': {
		'teacher_name': '丁利',
		'title': Teacher.TITLE[2][0],
		'department': Department.objects.get(name='LAW')
		}
	    },
	{
	    'user': {
		'username': 'hxl',
		'password': 'hxl',
		},
	    'teacher': {
		'teacher_name': '贺熊雷',
		'title': Teacher.TITLE[2][0],
		'department': Department.objects.get(name='BIO')
		}
	    },
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
    
## Administrator
from administrator.models import Administrator
admins = [
    {
        'user': {
            'username': 'admini',
            'password': 'admini',
        },
        'administrator': {
            'administrator_name': '我是传奇',
        }
    }        
]

Administrator.objects.all().delete()
for ad in admins:
    try:
        user = User.objects.get(username=ad['user']['username'])
    except User.DoesNotExist:
        user = User.objects.create_user(**ad['user'])
        user.save()
    adm = Administrator.objects.get_or_create(user=user, **ad['administrator'])
    if not adm[1]:
        print 'Administrator', adm[0].administrator_name, 'exists'
    else:
        print 'Creating Administrator', adm[0].administrator_name
        adm[0].save()

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
            },
	{
            'time': [
                {
                    'week': 2,
                    'time': 'CDE',
                    'location': '东C401'
                    }
                ],
            'course': {
                'name': 'IT项目管理',
                'academic_year': '2012-2013',
                'semester': 1,
                'from_week': 1,
                'to_week': 18,
                'teacher': Teacher.objects.get(teacher_name='李文军'),
                'credit': 3,
                'capacity': 50,
                'hastaken': 0,
                'exam_method': '笔试',
                'course_type':
                    CourseType.objects.get(type_name=CourseType.COURSE_TYPE[3][0]),
                'department': Department.objects.get(name='CS')
                }
            },
	{
            'time': [
                {
                    'week': 5,
                    'time': 'HI',
                    'location': '东A202'
                    }
                ],
            'course': {
                'name': '博弈论',
                'academic_year': '2012-2013',
                'semester': 1,
                'from_week': 2,
                'to_week': 13,
                'teacher': Teacher.objects.get(teacher_name='丁利'),
                'credit': 3,
                'capacity': 100,
                'hastaken': 0,
                'exam_method': '考察',
                'course_type':
                    CourseType.objects.get(type_name=CourseType.COURSE_TYPE[1][0]),
                'department': Department.objects.get(name='LAW')
                }
            },
	{
            'time': [
                {
                    'week': 1,
                    'time': 'IJK',
                    'location': '东A301'
                    }
                ],
            'course': {
                'name': '转基因研究',
                'academic_year': '2012-2013',
                'semester': 1,
                'from_week': 2,
                'to_week': 13,
                'teacher': Teacher.objects.get(teacher_name='贺熊雷'),
                'credit': 3,
                'capacity': 100,
                'hastaken': 0,
                'exam_method': '考察',
                'course_type':
                    CourseType.objects.get(type_name=CourseType.COURSE_TYPE[1][0]),
                'department': Department.objects.get(name='BIO')
                }
            },
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
