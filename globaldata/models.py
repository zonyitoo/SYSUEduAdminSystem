from django.db import models

# Create your models here.
class GlobalData(models.Model):
    pub_course_stage = models.PositiveSmallIntegerField(default=1)
    pub_elective_stage = models.PositiveSmallIntegerField(default=1)
    pro_course_stage = models.PositiveSmallIntegerField(default=1)
    pro_elective_stage = models.PositiveSmallIntegerField(default=1)

