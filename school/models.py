from django.db import models

class School(models.Model):
    name = models.CharField(max_length=30)
    addr = models.CharField(max_length=120)

class Department(models.Model):
    name = models.CharField(max_length=30)
    addr = models.CharField(max_length=120)
    school = models.ForeignKey(School)

class Profession(models.Model):
    name = models.CharField(max_length=30)
    department = models.ForeignKey(Department)
    
