#!/usr/bin/env python

import os, sys

PROJECT_PATH = './'

PROJECT_PATH = os.path.abspath(PROJECT_PATH)

if PROJECT_PATH not in sys.path:
    sys.path.append(PROJECT_PATH)

print "PATH=" + str(sys.path)

from EduAdminSystem import settings
from django.core.management import setup_environ
setup_environ(settings)


import createSchoolData
import createGlobalData
import createStudentData
import createAdminData
import createTeacherData
import createCourseData
import createAssessmentData
import createTakeData
