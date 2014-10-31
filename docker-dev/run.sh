#!/bin/bash

docker kill healthsites-postgis-dev
docker rm healthsites-postgis-dev
docker run --restart="always" --name="healthsites-postgis-dev" -d -t kartoza/postgis

docker kill healthsites-django-dev
docker rm healthsites-django-dev
docker run --name="healthsites-django-dev" -d -t konektaz/healthsitesdev
