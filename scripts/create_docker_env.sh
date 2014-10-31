#!/bin/bash

# First lets get Postgis going

#docker build -t kartoza/postgis git://github.com/kartoza/docker-postgis

#docker kill healthsites-postgis
#docker rm healthsites-postgis
docker run \
    --restart="always" \
    --name="healthsites-postgis" \
    --hostname="healthsites-postgis" \
    -d -t kartoza/postgis
# Make some time for db setup etc
sleep 10
# Now build the django image

cd docker-prod
./build.sh
cd ..

# Now collect migrate and collect static

OPTIONS="-e DATABASE_NAME=gis -e DATABASE_USERNAME=docker -e DATABASE_PASSWORD=docker -e DATABASE_HOST=healthsites-postgis -e DJANGO_SETTINGS_MODULE=core.settings.prod_docker"

docker run \
    --rm \
    --name="healthsites-migrate" \
    --hostname="healthsites-migrate" \
    ${OPTIONS} \
    --link healthsites-postgis:healthsites-postgis \
    -v /home/${USER}/production-sites/healthsites:/home/web \
    --entrypoint="/usr/bin/python" \
    -i -t konektaz/healthsites \
     /home/web/django_project/manage.py migrate


docker run \
    --rm \
    --name="healthsites-collect" \
    --hostname="healthsites-collect" \
    ${OPTIONS} \
    --link healthsites-postgis:healthsites-postgis \
    -v /home/${USER}/production-sites/healthsites:/home/web \
    --entrypoint="/usr/bin/python" \
    -i -t konektaz/healthsites \
    /home/web/django_project/manage.py collectstatic --noinput

# Now run the service

docker kill healthsites-django
docker rm healthsites-django
docker run \
    --restart="always" \
    --name="healthsites-django" \
    --hostname="healthsites-django" \
    ${OPTIONS} \
    --link healthsites-postgis:healthsites-postgis \
    -v /home/${USER}/production-sites/healthsites:/home/web \
    -v /tmp/healthsites-tmp:/tmp/healthsites-tmp \
    -p 49360:49360 \
    -d -t konektaz/healthsites
