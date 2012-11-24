# -*- coding:utf-8 -*-
from django.db import models
from teacher.models import Teacher
from school.models import Department

class CourseMeta(models.Model):
    description = models.TextField()
    submit_addr = models.URLField()

class CourseType(models.Model):
    PUB_COURSE = 'PubC'
    PUB_ELECTIVE = 'PubE'
    PRO_COURSE = 'ProC'
    PRO_ELECTIVE = 'ProE'
    COURSE_TYPE = (
            (PUB_COURSE, u'公共必修课'), 
            (PUB_ELECTIVE, u'公共选修课'), 
            (PRO_COURSE, u'专业必修课'), 
            (PRO_ELECTIVE, u'专业选修课'),
        )
    courseTypeToUnicode = {
            PUB_COURSE: u'公共必修课',
            PUB_ELECTIVE: u'公共选修课', 
            PRO_COURSE: u'专业必修课',
            PRO_ELECTIVE: u'专业选修课'
        }

    type_name = models.CharField(max_length=4, choices=COURSE_TYPE)

    def get_coursetype(self):
        return self.courseTypeToUnicode[self.type_name]
    
    def __unicode__(self):
        return self.courseTypeToUnicode[self.type_name]

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
    course_time = models.CharField(max_length=5)
    teacher = models.ForeignKey(Teacher)
    credit = models.PositiveSmallIntegerField()
    location = models.CharField(max_length=10)
    capacity = models.PositiveIntegerField()
    exam_method = models.CharField(max_length=20)
    course_type = models.ForeignKey(CourseType)
    course_meta = models.ForeignKey(CourseMeta, blank=True, null=True)
    department = models.ForeignKey(Department, default=0)
    assessment_avgscore = models.DecimalField(max_digits=5, decimal_places=2,
            default=0)
    assessment_num = models.IntegerField(default=0)
    
    def __unicode__(self):
        return self.name
