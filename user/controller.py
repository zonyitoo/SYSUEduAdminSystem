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

    newstudent = Student.objects.create(username=number, student_name=name, student_meta=meta)
    newstudent.set_password(password)
    newstudent.save()

    group.user_set.add(newstudent)
