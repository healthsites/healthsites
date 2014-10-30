#!/bin/bash

docker kill healthsites-postgis
docker rm healthsites-postgis
docker run --restart="always" --name="healthsites-postgis" -d -t kartoza/postgis


docker kill healthsites-postgis
docker rm healthsites-postgis
docker run --name="healthsites-postgis" -d -t konektaz/healthsites
