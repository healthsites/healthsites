#!/bin/bash

# First lets get Postgis going
source ${BASH_SOURCE%/*}/functions.sh

#docker build -t kartoza/postgis git://github.com/kartoza/docker-postgis

restart_postgis_server

# Now build the django image

cd ../docker-prod
./build.sh
cd -

# Now collect migrate and collect static
manage migrate
manage "collectstatic --noinput"

# Now run the service
run_django_server
# For debugging to see if uwsgi is running nicely before adding nginx
#run_django_server --protocol=http
