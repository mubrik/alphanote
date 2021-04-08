#!/bin/sh
PYTHONPATH=/var/app/venv/*/bin

# PYTHONPATH is available as EC2 instance environment variable
source "$PYTHONPATH/activate" && {
    # log with migrations have been applied
    python manage.py showmigrations;

    # run migrate
    python manage.py migrate --noinput;
}

source "$PYTHONPATH/activate" && {
    # run collectstatic
    python manage.py collectstatic --noinput;
}

source "$PYTHONPATH/activate" && {
    # run custom createsu script 
    python manage.py createsu;
}