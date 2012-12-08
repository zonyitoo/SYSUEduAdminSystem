#-*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from school.models import Speciality, Class

class StudentMinor(models.Model):
    minor = models.ForeignKey(Class)
    pubcourse_credit = models.PositiveIntegerField(default=0)
    pubelective_credit = models.PositiveIntegerField(default=0)
    procourse_credit = models.PositiveIntegerField(default=0)
    proelective_credit = models.PositiveIntegerField(default=0)
    pubcourse_weightsum = models.PositiveIntegerField(default=0)
    pubelective_weightsum = models.PositiveIntegerField(default=0)
    procourse_weightsum = models.PositiveIntegerField(default=0)
    proelective_weightsum = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return self.minor.name

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
    major = models.ForeignKey(Class)

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

def calGPA(score):
    score = score * 1.0
    if score < 60:
        return 0.0
    return (score - 50) / 10

class Student(models.Model):
    student_name = models.CharField(max_length=30)
    pubcourse_credit = models.PositiveIntegerField(default=0)
    pubelective_credit = models.PositiveIntegerField(default=0)
    procourse_credit = models.PositiveIntegerField(default=0)
    proelective_credit = models.PositiveIntegerField(default=0)
    pubcourse_weightsum = models.PositiveIntegerField(default=0)
    pubelective_weightsum = models.PositiveIntegerField(default=0)    
    procourse_weightsum = models.PositiveIntegerField(default=0)
    proelective_weightsum = models.PositiveIntegerField(default=0)
    student_meta = models.ForeignKey(StudentMeta)
    student_minor = models.ManyToManyField(StudentMinor, null=True, blank=True)
    user = models.OneToOneField(User, related_name='student')

    def __unicode__(self):
        return self.student_name


    def getDataDict(self):
        dc = {
            'user': self.user,
            'student_name': self.student_name,
            'pubcourse_credit': self.pubcourse_credit,
            'pubelective_credit': self.pubelective_credit,
            'procourse_credit': self.procourse_credit,
            'proelective_credit': self.proelective_credit,
            'student_meta': self.student_meta.getDataDict(),
            'user': {
                'username': self.user.username,
                'last_login': self.user.last_login,
            }
        }

        try:
            dc['gpa'] = str(calGPA((self.pubcourse_weightsum + self.pubelective_weightsum \
                        + self.procourse_weightsum + self.proelective_weightsum) \
                        / (self.pubcourse_credit + self.pubelective_credit \
                        + self.procourse_credit + self.proelective_credit))),
        except:
            dc['gpa'] = '0.0'
        try:
            dc['pubcourse_gpa'] = str(calGPA(self.pubcourse_weightsum / self.pubcourse_credit))
        except:
            dc['pubcourse_gpa'] = '0.0'
        try:
            dc['pubelective_gpa'] = str(calGPA(self.pubelective_weightsum / self.pubelective_credit))
        except:
            dc['pubelective_gpa'] = '0.0'
        try:
            dc['procourse_gpa'] = str(calGPA(self.procourse_weightsum / self.procourse_credit))
        except:
            dc['procourse_gpa'] = '0.0'
        try:
            dc['proelective_gpa'] = str(calGPA(self.proelective_weightsum / self.proelective_credit))
        except:
            dc['proelective_gpa'] = '0.0'

        return dc
