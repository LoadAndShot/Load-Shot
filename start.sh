#!/bin/bash
python manage.py migrate
gunicorn loadandshot.wsgi:application --bind 0.0.0.0:$PORT

