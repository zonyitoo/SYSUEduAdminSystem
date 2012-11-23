# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from school.models import Department
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
    img_addr = models.URLField(null=True, blank=True)
    site = models.URLField(null=True, blank=True)
    department = models.ForeignKey(Department)
    user = models.OneToOneField(User, related_name='teacher')

    def __unicode__(self):
        return self.teacher_name
