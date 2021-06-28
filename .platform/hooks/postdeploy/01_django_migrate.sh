#!/bin/bash

TASKS_DIR=/opt/elasticbeanstalk/tasks

# including django log in bundle logs
# log file in env var
echo "${LOG_FILE_PATH//.log/*}" > "$TASKS_DIR/bundlelogs.d/01-app-log.conf"
# include current app log file in tail logs
echo $LOG_FILE_PATH > "$TASKS_DIR/taillogs.d/01-app-log.conf"

source "$PYTHONPATH/activate" && {
# log which migrations have already been applied
python manage.py showmigrations;
# migrate
python manage.py migrate --noinput;

# create super user
python manage.py createsu;

# collectstatic
python manage.py collectstatic --noinput;
}