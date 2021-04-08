#!/bin/bash

# PYTHONPATH is available as EC2 instance environment variable
source "$PYTHONPATH/activate" && {
    # run custom createsu script 
    python manage.py createsu;
}