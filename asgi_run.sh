#!/bin/bash

rm ./server/migrations/0001_initial.py

python manage.py makemigrations

python manage.py migrate

daphne -e ssl:8443:privateKey=/etc/letsencrypt/live/ziho-dev.com/privkey.pem: certKey=/etc/letsencrypt/live/ziho-dev.com/cert.pem config.asgi:application