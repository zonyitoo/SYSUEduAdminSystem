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

## Assessment
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
