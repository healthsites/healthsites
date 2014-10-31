#!/bin/bash

# First lets get Postgis going
source functions.sh

docker build -t kartoza/postgis git://github.com/kartoza/docker-postgis

restart_postgis_server

# Now build the django image

cd docker-prod
./build.sh
cd ..

# Now collect migrate and collect static

migrate
collectstatic

# Now run the service

run_django_server
