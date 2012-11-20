from user.models import *
from school.models import Speciality
from django.contrib.auth.models import Group, User

def create_student(number, name, password, edutype, year, speciality):
    group = Group.objects.get_or_create(name='Student')[0] 
    speciality = Speciality.objects.get(name=speciality)
    meta = StudentMeta.objects.get_or_create(type_name=edutype, year=year,
            major=speciality)[0]

    user = User.objects.create(username=number)
    user.set_password(password)
    user.save()
    newstudent = Student.objects.create(student_name=name, student_meta=meta,
            user=user)
    newstudent.save()

    group.user_set.add(user)
    group.save()
