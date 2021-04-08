#!/bin/sh
source /var/app/venv/*/bin/activate
cd /var/app/staging

python manage.py showmigrations;
python manage.py migrate --noinput;
python manage.py collectstatic --noinput;
python manage.py createsu;