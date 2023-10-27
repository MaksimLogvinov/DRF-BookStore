#!/bin/bash
python manage.py makemigrations &&
python manage.py migrate &&
python manage.py collectstatic --no-input --clear &&
uwsgi --ini ./uwsgi.ini