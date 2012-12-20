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
    {
	'name': 'GYM_ELECTIVE',
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
