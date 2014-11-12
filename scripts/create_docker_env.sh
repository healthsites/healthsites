#!/bin/bash


# First lets get Postgis going
source ${BASH_SOURCE%/*}/functions.sh

restart_postgis_server
restart_qgis_server

# Now collect migrate and collect static
manage migrate
manage collectstatic --noinput

# Now run the service
run_django_server
# For debugging to see if uwsgi is running nicely before adding nginx
#run_django_server --protocol=http
