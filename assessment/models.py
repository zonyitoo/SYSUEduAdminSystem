from django.db import models
from course.models import Course
#from django.contrib.comments.models import Comment

class Assessment(models.Model):
    subject = models.PositiveSmallInteger()
    weight = models.PositiveSmallInteger()
    score = models.PositiveSmallInteger()
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return self.course.name

