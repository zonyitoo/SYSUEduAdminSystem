#-*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from school.models import Speciality, Department

class StudentMinor(models.Model):
    minor_speciality = models.ForeignKey(Speciality)
    pubcourse_credit = models.PositiveIntegerField(default=0)
    pubelective_credit = models.PositiveIntegerField(default=0)
    procourse_credit = models.PositiveIntegerField(default=0)
    proelective_credit = models.PositiveIntegerField(default=0)

class StudentMeta(models.Model):
    UNGRADUATED = 'UG'
    GRADUATED = 'G'
    STUDENT_TYPE = (
            (UNGRADUATED, u'本科生'), 
            (GRADUATED, u'研究生'), 
        )
    type_name = models.CharField(max_length=2, choices=STUDENT_TYPE, default=UNGRADUATED)
    year = models.CharField(max_length=4)
    req_pubcourse = models.PositiveIntegerField(default=0)
    req_pubelective = models.PositiveIntegerField(default=0)
    req_procourse = models.PositiveIntegerField(default=0)
    req_proelective = models.PositiveIntegerField(default=0)
    major = models.ForeignKey(Speciality)

class Student(models.Model):
    student_name = models.CharField(max_length=30)
    pubcourse_credit = models.PositiveIntegerField(default=0)
    pubelective_credit = models.PositiveIntegerField(default=0)
    procourse_credit = models.PositiveIntegerField(default=0)
    proelective_credit = models.PositiveIntegerField(default=0)
    grade_point = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    student_meta = models.ForeignKey(StudentMeta)
    student_minor = models.ManyToManyField(StudentMinor)
    user = models.OneToOneField(User, related_name='student')

    def __unicode__(self):
        return self.student_name

class Teacher(models.Model):
    teacher_name = models.CharField(max_length=30)
    TITLE_LECTURER = 'L'
    TITLE_ASSOCIATE_PROFESSOR = 'AP'
    TITLE_PROFESSOR = 'P'
    TITLE = (
            (TITLE_LECTURER, u'讲师'), 
            (TITLE_ASSOCIATE_PROFESSOR, u'副教授'), 
            (TITLE_PROFESSOR, u'教授'), 
        )
    title = models.CharField(max_length=2, choices=TITLE)
    img_addr = models.URLField(null=True)
    site = models.URLField(null=True)
    department = models.ForeignKey(Department)
    user = models.OneToOneField(User, related_name='teacher')

    def __unicode__(self):
        return self.teacher_name
