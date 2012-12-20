#!/usr/bin/env python
# -*- coding:utf-8 -*-

from EduAdminSystem import settings
from django.core.management import setup_environ
setup_environ(settings)
from django.contrib.auth.models import User, Group, Permission
from school.models import School, Department, Speciality, Class
from student.models import Student, StudentMeta
from course.models import Course

"""
    This script just for generating test data.
    If you get runtime errors, you can
        1. Drop eduadminsystemdb database and recreate it
        2. Debug this script

    Thie script will delete all your remain data
"""
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
            ct = obj[0].course.course_type
            cred = obj[0].course.credit
            mark = obj[0].score * cred
            if ct == 'PubC' or ct == 'GymE':
                obj[0].student.pubcourse_credit += cred
                obj[0].student.pubcourse_weightsum += mark
            elif ct == 'PubE':
                obj[0].student.pubelective_credit += cred
                obj[0].student.pubelective_weightsum += mark
            elif ct == 'ProC':
                obj[0].student.procourse_credit += cred
                obj[0].student.procourse_weightsum += mark
            elif ct == 'ProE':
                obj[0].student.proelective_credit += cred
                obj[0].student.proelective_weightsum += mark
            obj[0].student.save()
        obj[0].course.save()
        obj[0].save()
