#!/bin/bash

# PYTHONPATH is available as EC2 instance environment variable
source "$PYTHONPATH/activate" && {
    # log with migrations have been applied
    python manage.py showmigrations;

    # run migrate
    python manage.py migrate --noinput;
}