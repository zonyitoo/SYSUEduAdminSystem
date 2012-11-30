from django.db import models
from course.models import Course
from student.models import Student

class Takes(models.Model):
    course = models.ForeignKey(Course)
    student = models.ForeignKey(Student)
    usual_score = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    final_score = models.DecimalField(max_digits=4, decimal_places=1, default=0)
    final_percentage = models.PositiveSmallIntegerField(default=60)
    has_assessment = models.BooleanField(default=False)
    screened = models.BooleanField(default=False)
    rank = models.PositiveIntegerField(default=0, blank=True)
    
    def __unicode__(self):
        return self.student, self.course

    def getDataDict(self):
        return {
            'coures': self.course.getDataDict(),
            'student': self.student.getDataDict(),
            'usual_score': self.usual_score,
            'final_score': self.final_score,
            'final_percentage': self.final_percentage,
            'has_assessment': self.has_assessment,
            'screened': self.screened,
            'rank': self.rank,
        }
