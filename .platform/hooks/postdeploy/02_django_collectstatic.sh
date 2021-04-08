#!/bin/bash

# PYTHONPATH is available as EC2 instance environment variable
source "$PYTHONPATH/activate" && {
    # run collectstatic
    python manage.py collectstatic --noinput;
}