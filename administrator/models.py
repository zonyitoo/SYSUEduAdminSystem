from django.db import models
from django.contrib.auth.models import User
from school.models import School

class Administrator(models.Model):
    administrator_name = models.CharField(max_length=30)
    school = models.ForeignKey(School, null=True)
    user = models.OneToOneField(User, related_name='administrator')
