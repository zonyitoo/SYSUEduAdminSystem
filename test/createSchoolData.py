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
from school.models import School, Department, Speciality, Class

schools = [
    {
        'name': '信息科学与技术学院'
        },
    {
        'name': '软件学院'
        },
    {
	    'name': '法学院'
	    },
    {
	    'name': '生命科学学院'
	    },
    {
        'name': 'TEST'
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
        'name': '计算机科学系',
        'school': School.objects.get(name='信息科学与技术学院')
        },
    {
	    'name': '软件工程',
	    'school': School.objects.get(name='软件学院')
	    },
    {
	    'name': 'TEST',
	    'school': School.objects.get(name='TEST')
	    },
    {
	    'name': '法学',
	    'school': School.objects.get(name='法学院')
	    },
    {
	    'name': '生物科学与技术系',
	    'school': School.objects.get(name='生命科学学院')
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
        'name': '计算机科学与技术',
        'department': Department.objects.get(name='计算机科学系')
        },        
    {
        'name': 'TEST',
        'department': Department.objects.get(name='TEST')
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
        'speciality': Speciality.objects.get(name='计算机科学与技术'),
        },
    {
        'name': '计算机B班',
        'speciality': Speciality.objects.get(name='计算机科学与技术'),
        },
    {
        'name': '主体思想班',
        'speciality': Speciality.objects.get(name='TEST'),
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
