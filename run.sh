#!/bin/bash

rm ./server/migrations/0001_initial.py

python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic

gunicorn config.wsgi -b 0.0.0.0:8000