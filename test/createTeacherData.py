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
                'teacher_name': '纪庆革',
                'title': Teacher.TITLE[1][0],
                'department': Department.objects.get(name='计算机科学系')
                }
            },
        {
            'user': {
                'username': 'yy',
                'password': 'yy',
                },
            'teacher': {
                'teacher_name': '衣杨',
                'title': Teacher.TITLE[1][0],
                'department': Department.objects.get(name='计算机科学系')
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
                'department': Department.objects.get(name='计算机科学系')
                }
            },
        {
            'user': {
                'username': 'naive',
                'password': 'naive',
                },
            'teacher': {
                'teacher_name': '贝叶斯',
                'title': Teacher.TITLE[2][0],
                'department': Department.objects.get(name='计算机科学系')
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
		'department': Department.objects.get(name='软件工程')
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
		'department': Department.objects.get(name='法学')
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
		'department': Department.objects.get(name='生物科学与技术系')
		}
	    },
	{
	    'user': {
		'username': 'mks',
		'password': 'mks',
		},
	    'teacher': {
		'teacher_name': '马克思',
		'title': Teacher.TITLE[2][0],
		'department': Department.objects.get(name='TEST')
		}
	    },
    ]

for i in range(2000001, 2000011):
    d = {
            'user': {
                'username': str(i),
                'password': '123456',
            },
            'teacher': {
                'teacher_name': str(i),
                'title': Teacher.TITLE[i%3][0],
                'department': Department.objects.get(name='计算机科学系')
            }
        }
    teachers.append(d)

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
