#!/bin/bash

rm ./server/migrations/0001_initial.py

python manage.py makemigrations

python manage.py migrate
