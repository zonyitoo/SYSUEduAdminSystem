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
## Global Data
from globaldata.models import GlobalData

data = [
    {
	'name': 'PUB_COURSE',
        'stage': 1,
        },
    {
	'name': 'PUB_ELECTIVE',
        'stage': 1,
        },
    {
	'name': 'PRO_COURSE',
        'stage': 1,
        },
    {
	'name': 'PRO_ELECTIVE',
        'stage': 1,
        },

]

GlobalData.objects.all().delete()

for d in data:
    obj = GlobalData.objects.get_or_create(**d)
    if not obj[1]:
        print 'GlobaData exists'
    else:
        print 'Creating GlobalData'
        obj[0].save()

## Schools
from school.models import School, Department, Speciality, Class

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

classes = [
    {
        'name': '计算机A班',
        'speciality': Speciality.objects.get(name='CST'),
        },
    {
        'name': '计算机B班',
        'speciality': Speciality.objects.get(name='CST'),
        },
]

Class.objects.all().delete()
for c in classes:
    obj = Class.objects.get_or_create(**c)
    if not obj[1]:
        print 'Class', c['name'], 'exists'
    else:
        print 'Creating Class', c['name']
        obj[0].save()

# Students
from student.models import Student, StudentMeta

studentMetas = [
    {
        'type_name': StudentMeta.UNGRADUATED,
        'year': '2010',
        'major': Class.objects.get(name='计算机A班'),
        'req_pubcourse': 34,
        'req_pubelective': 16,
        'req_procourse': 75,
        'req_proelective': 32,
    },
    {
        'type_name': StudentMeta.UNGRADUATED,
        'year': '2010',
        'major': Class.objects.get(name='计算机B班'),
        'req_pubcourse': 34,
        'req_pubelective': 16,
        'req_procourse': 75,
        'req_proelective': 32,
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
            major=Class.objects.get(name='计算机A班'), year=2010)
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
            major=Class.objects.get(name='计算机A班'), year=2010)
        }
    },
    {
    "user": {
        "username": "10383003",
        "password": "123456",
        },
    "student": {
        "student_name": "崔成浩",
        "student_meta": StudentMeta.objects.get(
            major=Class.objects.get(name='计算机A班'), year=2010)
        }
    },
    {
    "user": {
        "username": "10383073",
        "password": "123456",
        },
    "student": {
        "student_name": "金正恩",
        "student_meta": StudentMeta.objects.get(
            major=Class.objects.get(name='计算机B班'), year=2010)
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
             major=Class.objects.get(name='计算机B班'), year=2010)
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
from course.models import Course, CourseTime
from assessment.models import Assessment, AssessmentEntry, AssessmentSubject
asssubjs = [
    ## Type 1
    {
        'assessment_type': 1,
        'description': '教学态度',
    },
    {
        'assessment_type': 1,
        'description': '教学内容',
    },
    {
        'assessment_type': 1,
        'description': '教学方法',
    },
    {
        'assessment_type': 1,
        'description': '教学效果',
    },
    ## Type 2
    {
        'assessment_type': 2,
        'description': '教学态度',
    },
    {
        'assessment_type': 2,
        'description': '教学内容',
    },
    {
        'assessment_type': 2,
        'description': '教学方法',
    },
    {
        'assessment_type': 2,
        'description': '教学效果',
    },
    ## Type 3
    {
        'assessment_type': 3,
        'description': '教学态度',
    },
    {
        'assessment_type': 3,
        'description': '教学内容',
    },
    {
        'assessment_type': 3,
        'description': '教学方法',
    },
    {
        'assessment_type': 3,
        'description': '教学效果',
    },
    ## Type 4
    {
        'assessment_type': 4,
        'description': '教学态度',
    },
    {
        'assessment_type': 4,
        'description': '教学内容',
    },
    {
        'assessment_type': 4,
        'description': '教学方法',
    },
    {
        'assessment_type': 4,
        'description': '教学效果',
    },
]

AssessmentSubject.objects.all().delete()
for ass in asssubjs:
    asb = AssessmentSubject.objects.get_or_create(**ass)
    if asb[1]:
        print "Creating Assessment Subject", ass
        asb[0].save()

assentries = [
    ## Type 3
    {
        'subject': AssessmentSubject.objects.get(assessment_type=3,
            description='教学态度'),
        'description': "备课充分，授课熟练。",
        'weight': 2,
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=3, 
            description='教学态度'),
        'description': "教态大方，为人师表。",
        'weight': 2,
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=3,
            description='教学态度'),
        'description': "愿意与学生交流，能耐心解答学生疑问。",
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=3,
            description='教学内容'),
        'description': "讲课深度和容量适合学生掌握。",
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=3,
            description='教学内容'),
        'description': "内容清晰，重点突出，难点讲透。",
        'weight': 2,
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=3,
            description='教学内容'),
        'description': "注重反映学科发展的新动态和新成果。",
        'weight': 2,
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=3,
            description='教学内容'),
        'description': "能介绍相关参考资料，注意新旧内容衔接。",
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=3,
            description='教学方法'),
        'description': "联系实际，案例讲解与理论阐述结合恰当。",
        'weight': 2,
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=3,
            description='教学方法'),
        'description': "讲课有启发性，善于促进学生思考。",
        'weight': 2,
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=3,
            description='教学方法'),
        'description': "能采用多种教学手段，运用效果好。",
        'weight': 2,
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=3,
            description='教学效果'),
        'description': "教师授课有助于提高学生的认识、分析和解决问题的能力。",
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=3,
            description='教学效果'),
        'description': "教师授课有利于提高学生的学习兴趣。",
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=3,
            description='教学效果'),
        'description': "教师授课有助于引导学生自学。",
    },
    ## Type 4
    {
        'subject': AssessmentSubject.objects.get(assessment_type=4,
            description='教学态度'),
        'description': "教书育人，为人师表。",
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=4,
            description='教学态度'),
        'description': "实验教学准备充分，讲课流利。",
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=4,
            description='教学态度'),
        'description': "批改实验报告及时、认真，辅导耐心。",
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=4,
            description='教学内容'),
        'description': "熟悉实验内容和仪器使用，指导材料齐备。",
        'weight': 2,
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=4,
            description='教学内容'),
        'description': "内容设计合理、讲解清晰，示范准确、规范。",
        'weight': 2,
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=4,
            description='教学内容'),
        'description': "能安排一定的综合性、设计性的实验内容，并将科研成果引入教学。",
        'weight': 2,
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=4,
            description='教学方法'),
        'description': "教学组织手段灵活有效、教学秩序好。",
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=4,
            description='教学方法'),
        'description': "善于引导学生运用所学知识分析实验的现象和结果。",
        'weight': 2,
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=4,
            description='教学方法'),
        'description': "善于启发学生思考，注重师生互动。",
        'weight': 2,
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=4,
            description='教学效果'),
        'description': "有助于培养学生的创新意识和创新思维。",
        'weight': 2,
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=4,
            description='教学效果'),
        'description': "有助于提高学生的实验动手能力。",
        'weight': 2,
    },
    {
        'subject': AssessmentSubject.objects.get(assessment_type=4,
            description='教学效果'),
        'description': "有助于学生巩固相关的理论知识。",
        'weight': 2,
    },
]

AssessmentEntry.objects.all().delete()
for assentry in assentries:
	ae = AssessmentEntry.objects.get_or_create(**assentry)
	if ae[1]:
		print "Creating Assessment Entry", assentry
		ae[0].save()

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
                'course_type': Course.PRO_ELECTIVE,
                'department': Department.objects.get(name='CS'),
                'class_oriented': Class.objects.get(name='计算机B班'),
                'assessment_type': Course.ASSTYPE_THEORY,
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
                'course_type': Course.PRO_ELECTIVE,
                'department': Department.objects.get(name='CS'),
                'class_oriented': Class.objects.get(name='计算机A班'),
                'assessment_type': Course.ASSTYPE_THEORY,
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
                'course_type': Course.PRO_ELECTIVE,
                'department': Department.objects.get(name='CS'),
                'class_oriented': Class.objects.get(name='计算机B班'),
                'assessment_type': Course.ASSTYPE_THEORY,
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
                'course_type': Course.PRO_COURSE,
                'department': Department.objects.get(name='CS'),
                'class_oriented': Class.objects.get(name='计算机B班'),
                'assessment_type': Course.ASSTYPE_THEORY,
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
                'course_type': Course.PUB_COURSE,
                'department': Department.objects.get(name='CS'),
                'class_oriented': Class.objects.get(name='计算机A班'),
                'assessment_type': Course.ASSTYPE_THEORY,
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
                'capacity': 1,
                'hastaken': 0,
                'exam_method': '笔试',
                'course_type': Course.PUB_ELECTIVE,
                'department': Department.objects.get(name='CS'),
                'class_oriented': Class.objects.get(name='计算机A班'),
                'assessment_type': Course.ASSTYPE_THEORY,
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
                'course_type': Course.PUB_ELECTIVE,
                'department': Department.objects.get(name='CS'),
                'class_oriented': Class.objects.get(name='计算机B班'),
                'assessment_type': Course.ASSTYPE_THEORY,
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
                'course_type': Course.PUB_ELECTIVE,
                'department': Department.objects.get(name='LAW'),
                'assessment_type': Course.ASSTYPE_THEORY,
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
                'course_type': Course.PUB_ELECTIVE,
                'department': Department.objects.get(name='BIO'),
                'assessment_type': Course.ASSTYPE_THEORY,
                }
            },
	{
            'time': [
                {
                    'week': 1,
                    'time': 'IJK',
                    'location': '东A405'
                    }
                ],
            'course': {
                'name': '法律史',
                'academic_year': '2012-2013',
                'semester': 1,
                'from_week': 2,
                'to_week': 13,
                'teacher': Teacher.objects.get(teacher_name='丁利'),
                'credit': 3,
                'capacity': 100,
                'hastaken': 0,
                'exam_method': '考察',
                'course_type': Course.PUB_ELECTIVE,
                'department': Department.objects.get(name='LAW'),
                'assessment_type': Course.ASSTYPE_THEORY,
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

        """
        if obj[0].assessment_type == Course.ASSTYPE_THEORY:
            for subi in range(1, 5):
                Assessment(subject=subi, course=obj[0], weight=25).save()
        """
        ## Other course type????

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
                'course': Course.objects.get(name='Test_Capacity1',
                    academic_year='2012-2013'),
                'student': Student.objects.get(student_name='崔成浩')
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
        if obj[0].score > 0:
            obj[0].course.hasscore = True
        obj[0].course.save()
        obj[0].save()
