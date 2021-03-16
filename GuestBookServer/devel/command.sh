#!/bin/sh

python manage.py runserver_plus --cert-file /opt/cert.crt 0.0.0.0:8000
# python manage.py runserver 0.0.0.0:8000