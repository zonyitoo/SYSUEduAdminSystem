#!/usr/bin/env python
# -*- coding:utf-8 -*-

from EduAdminSystem import settings
from django.core.management import setup_environ
setup_environ(settings)
from django.contrib.auth.models import User, Group, Permission
from school.models import School, Department, Speciality, Class
from globaldata.models import GlobalData
from teacher.models import Teacher
from course.models import Course, CourseTime

"""
    This script just for generating test data.
    If you get runtime errors, you can
        1. Drop eduadminsystemdb database and recreate it
        2. Debug this script

    Thie script will delete all your remain data
"""
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
                'teacher': Teacher.objects.get(teacher_name='激情哥'),
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
                'teacher': Teacher.objects.get(teacher_name='激情哥'),
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
                'teacher': Teacher.objects.get(teacher_name='杨毅'),
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
                'teacher': Teacher.objects.get(teacher_name='丘道长'),
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
                'teacher': Teacher.objects.get(teacher_name='Naive Bayes'),
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
                'teacher': Teacher.objects.get(teacher_name='Naive Bayes'),
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

