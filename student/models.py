#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from school.models import Speciality

class StudentMinor(models.Model):
    minor_speciality = models.ForeignKey(Speciality)
    pubcourse_credit = models.PositiveIntegerField(default=0)
    pubelective_credit = models.PositiveIntegerField(default=0)
    procourse_credit = models.PositiveIntegerField(default=0)
    proelective_credit = models.PositiveIntegerField(default=0)
    gpa = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    pubcourse_gpa = models.DecimalField(max_digits=2, decimal_places=1,
            default=0)
    pubelective_gpa = models.DecimalField(max_digits=2, decimal_places=1,
            default=0)
    procourse_gpa = models.DecimalField(max_digits=2, decimal_places=1,
            default=0)
    proelective_gpa = models.DecimalField(max_digits=2, decimal_places=1,
            default=0)

class StudentMeta(models.Model):
    UNGRADUATED = 'UG'
    GRADUATED = 'G'
    STUDENT_TYPE = (
            (UNGRADUATED, u'本科生'), 
            (GRADUATED, u'研究生'), 
        )
    TYPE_TO_UNICODE = {k: u for k, u in STUDENT_TYPE}

    type_name = models.CharField(max_length=2, choices=STUDENT_TYPE, default=UNGRADUATED)
    year = models.CharField(max_length=4)
    req_pubcourse = models.PositiveIntegerField(default=0)
    req_pubelective = models.PositiveIntegerField(default=0)
    req_procourse = models.PositiveIntegerField(default=0)
    req_proelective = models.PositiveIntegerField(default=0)
    major = models.ForeignKey(Speciality)

    def __unicode__(self):
        return self.TYPE_TO_UNICODE[self.type_name]

    def getUnicodeType(self):
        return self.TYPE_TO_UNICODE[self.type_name]

    def getDataDict(self):
        return {
            'type_name': self.TYPE_TO_UNICODE[self.type_name],
            'year': self.year,
            'req_pubcourse': self.req_pubcourse,
            'req_pubelective': self.req_pubelective,
            'req_procourse': self.req_procourse,
            'req_proelective': self.req_proelective,
            'major': self.major.getDataDict()
        }

class Student(models.Model):
    student_name = models.CharField(max_length=30)
    pubcourse_credit = models.PositiveIntegerField(default=0)
    pubelective_credit = models.PositiveIntegerField(default=0)
    procourse_credit = models.PositiveIntegerField(default=0)
    proelective_credit = models.PositiveIntegerField(default=0)
    gpa = models.DecimalField(max_digits=2, decimal_places=1, default=0)
    pubcourse_gpa = models.DecimalField(max_digits=2, decimal_places=1,
            default=0)
    pubelective_gpa = models.DecimalField(max_digits=2, decimal_places=1,
            default=0)
    procourse_gpa = models.DecimalField(max_digits=2, decimal_places=1,
            default=0)
    proelective_gpa = models.DecimalField(max_digits=2, decimal_places=1,
            default=0)
    student_meta = models.ForeignKey(StudentMeta)
    student_minor = models.ManyToManyField(StudentMinor, null=True, blank=True)
    user = models.OneToOneField(User, related_name='student')

    def __unicode__(self):
        return self.student_name

    def getDataDict(self):
        dc = {
            'student_name': self.student_name,
            'pubcourse_credit': self.pubcourse_credit,
            'pubelective_credit': self.pubelective_credit,
            'procourse_credit': self.procourse_credit,
            'proelective_credit': self.proelective_credit,
            'gpa': str(self.gpa),
            'pubcourse_gpa': str(self.pubcourse_gpa),
            'pubelective_gpa': str(self.pubelective_gpa),
            'procourse_gpa': str(self.procourse_gpa),
            'proelective_gpa': str(self.proelective_gpa),
            'student_meta': self.student_meta.getDataDict(),
        }

        return dc
