#!/usr/bin/env python
# -*- coding:utf-8 -*-

from EduAdminSystem import settings
from django.core.management import setup_environ
setup_environ(settings)
from django.contrib.auth.models import User, Group, Permission
from school.models import School, Department, Speciality, Class

"""
    This script just for generating test data.
    If you get runtime errors, you can
        1. Drop eduadminsystemdb database and recreate it
        2. Debug this script

    Thie script will delete all your remain data
"""
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

