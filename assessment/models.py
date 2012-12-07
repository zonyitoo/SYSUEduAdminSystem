from django.db import models
from course.models import Course
#from django.contrib.comments.models import Comment

class Assessment(models.Model):
    subject = models.PositiveSmallIntegerField()
    weight = models.PositiveSmallIntegerField()
    score = models.PositiveSmallIntegerField()
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return self.course.name
    
    def getDataDict(self):
        return {
            'subject': self.subject,
            'weight': self.weight,
            'score': self.score,
            'course': self.course.getDataDict(),
        }

