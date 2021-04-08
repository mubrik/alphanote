#!/bin/bash
TASKS_DIR=/opt/elasticbeanstalk/tasks
LOG_FILE_PATH=/tmp/django-app.log

# include all app log files into the bundle logs (relplaces ".log" by *)
echo ${LOG_FILE_PATH//.log/*} > $TASKS_DIR/bundlelogs.d/01-app-log.conf

# include current app log file in tail logs
echo $LOG_FILE_PATH > $TASKS_DIR/taillogs.d/01-app-log.conf