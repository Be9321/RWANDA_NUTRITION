#!/usr/bin/env bash
set -o errexit

python manage.py collectstatic --no-input
python manage.py migrate
python manage.py seed_demo
python manage.py seed_districts

