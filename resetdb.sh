#!/bin/sh

sudo -u postgres dropdb easdb
sudo -u postgres createdb easdb -O eas
python manage.py syncdb --noinput
#python createTestData.py
