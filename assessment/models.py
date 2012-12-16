from django.db import models
from course.models import Course
#from django.contrib.comments.models import Comment

# Major subject
class AssessmentSubject(models.Model):
    assessment_type = models.PositiveSmallIntegerField(default=0)
    description = models.TextField()

    def getDataDict(self):
        return {
            'assessment_type': self.assessment_type,
            'description': self.description,
        }

class AssessmentEntry(models.Model):
    subject = models.ForeignKey(AssessmentSubject)
    description = models.TextField()
    weight = models.PositiveSmallIntegerField(default=1)
    
    def getDataDict(self):
        return {
            #'subject': self.subject.getDataDict(),
            'description': self.description,
            'weight': self.weight,
        }

class Assessment(models.Model):
    entry = models.ForeignKey(AssessmentEntry)
    score = models.PositiveSmallIntegerField(default=0)
    course = models.ForeignKey(Course)

    def __unicode__(self):
        return self.course.name
    
    def getDataDict(self):
        return {
            'entry': self.entry.getDataDict(),
            'score': self.score,
            #'course': self.course.getDataDict(),
        }

