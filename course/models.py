# -*- coding:utf-8 -*-
from django.db import models
from teacher.models import Teacher
from school.models import Department, Class

class CourseMeta(models.Model):
    description = models.TextField()
    submit_addr = models.URLField()
    grade = models.CharField(max_length=4)

class CourseTime(models.Model):
    week = models.PositiveSmallIntegerField()
    time = models.CharField(max_length=15)
    location = models.CharField(max_length=10)

    def __unicode__(self):
        return str(self.week)

    def getDataDict(self):
        return {
            'week': self.week,
            'time': self.time,
            'place': self.location
        }
    
class Course(models.Model):
    name = models.CharField(max_length=30)
    academic_year = models.CharField(max_length=9)
    SEM_FIRST = 1
    SEM_SECOND = 2
    SEM_THIRD = 3
    SEMESTER = (
            (SEM_FIRST, u'第一学期'), 
            (SEM_SECOND, u'第二学期'), 
            (SEM_THIRD, u'第三学期'),
        )
    semester = models.PositiveSmallIntegerField(choices=SEMESTER)
    from_week = models.PositiveSmallIntegerField()
    to_week = models.PositiveSmallIntegerField()
    course_time = models.ManyToManyField(CourseTime)
    teacher = models.ForeignKey(Teacher)
    credit = models.PositiveSmallIntegerField()
    capacity = models.PositiveIntegerField()
    exam_method = models.CharField(max_length=20)

    PUB_COURSE = 'PubC'
    PUB_ELECTIVE = 'PubE'
    PRO_COURSE = 'ProC'
    PRO_ELECTIVE = 'ProE'
    COURSE_TYPE = (
            (PUB_COURSE, u'公必'), 
            (PUB_ELECTIVE, u'公选'), 
            (PRO_COURSE, u'专必'), 
            (PRO_ELECTIVE, u'专选'),
        )
    COURSE_TYPE_TO_UNICODE = { k:v for k, v in COURSE_TYPE }

    course_type = models.CharField(max_length=4, choices=COURSE_TYPE)
    course_meta = models.ForeignKey(CourseMeta, blank=True, null=True)
    attendance_percentage = models.PositiveSmallIntegerField(default=10)
    final_percentage = models.PositiveSmallIntegerField(default=60)
    hastaken = models.IntegerField(default=0)
    department = models.ForeignKey(Department)
    class_oriented = models.ForeignKey(Class, null=True)
    screened = models.BooleanField(default=False)
    stage = models.PositiveSmallIntegerField(default=1)
    hasscore = models.BooleanField(default=False)
    
    ASSTYPE_PHIL = 1
    ASSTYPE_GYM = 2
    ASSTYPE_THEORY = 3
    ASSTYPE_LAB = 4
    ASSTYPE_FOREIGN = 5
    ASSESSMENT_TYPE = (
        (ASSTYPE_PHIL, u'哲学类'),
        (ASSTYPE_GYM, u'体育类'),
        (ASSTYPE_THEORY, u'理论类'), 
        (ASSTYPE_LAB, u'实验类'),
        (ASSTYPE_FOREIGN, u'外语类'),
    )
    ASSTYPE_UNICODE = {x:y for x, y in ASSESSMENT_TYPE}

    assessment_type = models.PositiveSmallIntegerField(default=ASSTYPE_THEORY,
            choices=ASSESSMENT_TYPE)
    
    def __unicode__(self):
        return self.name
    
    def getDataDict(self):
        return {
            'id': self.id,
            'name': self.name,
            'academic_year': self.academic_year,
            'semester': self.semester,
            'from_week': self.from_week,
            'to_week': self.to_week,
            'course_time': [ct.getDataDict() for ct in self.course_time.all()],
            'teacher': self.teacher.getDataDict(),
            'credit': self.credit,
            'capacity': self.capacity,
            'exam_method': self.exam_method,
            'attendance_percentage': self.attendance_percentage,
            'final_percentage': self.final_percentage,
            'course_type': self.COURSE_TYPE_TO_UNICODE[self.course_type],
            'hastaken': self.hastaken,
            'department': self.department.getDataDict(),
            'screened': self.screened,
            'stage': self.stage,
            'assessment_type': self.assessment_type,
            'class_oriented': self.class_oriented.getDataDict() if
                self.class_oriented else None
        }

