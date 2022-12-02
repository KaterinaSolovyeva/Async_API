#!/usr/bin/env bash

set -e

python manage.py migrate

uwsgi --strict --ini uwsgi/uwsgi.ini
