#!/bin/sh

sudo -u postgres dropdb easdb
sudo -u postgres createdb easdb -O eas
python manage.py syncdb --noinput
python createGlobalData.py
python createSchoolData.py
python createStudentData.py
python createTeacherData.py
python createAdminData.py
python createAssessmentData.py
python createCourseData.py
python createTakeData.py
