#!/bin/bash

rm ./server/migrations/0001_initial.py

python manage.py makemigrations

python manage.py migrate

daphne -e ssl:8443:privateKey=privkey.pem: certKey=cert.pem config.asgi:application