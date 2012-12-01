from django.db import models
from course.models import Course
from student.models import Student

class Takes(models.Model):
    course = models.ForeignKey(Course)
    student = models.ForeignKey(Student)
    usual_score = models.PositiveIntegerField(default=0)
    final_score = models.PositiveIntegerField(default=0)
    score = models.PositiveIntegerField(default=0)
    has_assessment = models.BooleanField(default=False)
    screened = models.BooleanField(default=False)
    rank = models.PositiveIntegerField(default=0, blank=True)
    attendance = models.PositiveSmallIntegerField(default=100)
    
    def __unicode__(self):
        return self.student.student_name + ' ' + self.course.name

    def getDataDict(self):
        return {
            'course': self.course.getDataDict(),
            'student': self.student.getDataDict(),
            'usual_score': self.usual_score,
            'final_score': self.final_score,
            'score': self.score,
            'has_assessment': self.has_assessment,
            'screened': self.screened,
            'rank': self.rank,
            'attendance': self.attendance,
        }
