#!/bin/bash

docker kill healthsites-postgis
docker rm healthsites-postgis
docker run \
    --restart="always" \
    --name="healthsites-postgis" \
    --hostname="healthsites-postgis" \
    -d -t kartoza/postgis

docker kill healthsites-django
docker rm healthsites-django
docker run \
    --restart="always" \
    --name="healthsites-django" \
    --hostname="healthsites-django" \
    -e DATABASE_NAME=gis \
    -e DATABASE_USERNAME=docker \
    -e DATABASE_PASSWORD=docker \
    -e DATABASE_HOST=healthsites-postgis \
    --link healthsites-postgis:healthsites-postgis \
    -v /home/${USER}/production-sites/healthsites:/home/web \
    -v /tmp/healthsites-tmp:/tmp/healthsites-tmp \
    -p 49360:49360 \
    -d -t konektaz/healthsites
