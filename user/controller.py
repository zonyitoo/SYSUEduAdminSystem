from user.models import *
from school.models import Speciality
from django.contrib.auth.models import Group

def create_student(number, name, password, edutype, year, speciality):
    try:
        group = Group.objects.get(name='student')
    except Group.DoesNotExist:
        group = Group(name='student')
        group.save()
        
    speciality = Speciality.objects.get(name=speciality)

    try:
        meta = StudentMeta.objects.get(type_name=edutype, year=year, major=speciality)
    except StudentMeta.DoesNotExist:
        meta = StudentMeta(type_name=edutype, year=year, major=speciality)
        meta.save()

    newstudent = Student(username=number, student_name=name, password=password, student_meta=meta)
    newstudent.save()

    group.user_set.add(newstudent)
