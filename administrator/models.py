from django.db import models
from django.contrib.auth.models import User

class Adminstrator(models.Model):
    adminstrator_name = models.CharField(max_length=30)
    user = models.OneToOneField(User, related_name='adminstrator')
