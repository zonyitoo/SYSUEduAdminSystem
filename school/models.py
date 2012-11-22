from django.db import models

class School(models.Model):
    name = models.CharField(max_length=30)
    addr = models.CharField(max_length=120)

    def __unicode__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=30)
    addr = models.CharField(max_length=120)
    school = models.ForeignKey(School)

    def __unicode__(self):
        return self.name

class Speciality(models.Model):
    name = models.CharField(max_length=30)
    department = models.ForeignKey(Department)

    def __unicode__(self):
        return self.name
    
