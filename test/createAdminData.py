#!/usr/bin/env python
# -*- coding:utf-8 -*-

from django.contrib.auth.models import User, Group, Permission

"""
    This script just for generating test data.
    If you get runtime errors, you can
        1. Drop eduadminsystemdb database and recreate it
        2. Debug this script

    Thie script will delete all your remain data
"""
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
