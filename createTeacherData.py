#!/usr/bin/env python
# -*- coding:utf-8 -*-

from EduAdminSystem import settings
from django.core.management import setup_environ
setup_environ(settings)
from django.contrib.auth.models import User, Group, Permission
from school.models import School, Department, Speciality, Class
from teacher.models import Teacher

"""
    This script just for generating test data.
    If you get runtime errors, you can
        1. Drop eduadminsystemdb database and recreate it
        2. Debug this script

    Thie script will delete all your remain data
"""

## Teachers
teachers = [
        {
            'user': {
                'username': 'jqg',
                'password': 'jqg',
                },
            'teacher': {
                'teacher_name': '激情哥',
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
                'teacher_name': '杨毅',
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
                'teacher_name': '丘道长',
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
                'teacher_name': 'Naive Bayes',
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
