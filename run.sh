#!/bin/bash

rm ./server/migrations/0001_initial.py

python manage.py makemigrations

python manage.py migrate

python manage.py collectstatic

gunicorn config.wsgi -b 0.0.0.0:8000


daphne -e ssl:8000:privateKey=/etc/letsencrypt/live/catchi-nichi.tk/privkey.pem:certKey=/etc/letsencrypt/live/catchi-nichi.tk/fullchain.pem: config.asgi:application

