from django.db import models
from course.models import Course
from user.models import Student

class Takes(models.Model):
    course = models.ForeignKey(Course)
    student = models.ForeignKey(Student)
    usual_score = models.DecimalField(max_digits=4, decimal_places=1)
    final_score = models.DecimalField(max_digits=4, decimal_places=1)
    final_percentage = models.PositiveSmallIntegerField()
    has_assessment = models.BooleanField(default=False)
