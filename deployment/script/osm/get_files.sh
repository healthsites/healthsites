#!/usr/bin/env bash

DIRECTORY='/Users/etienne/dev/web/healthsites'
PROJECT_ID='osm_update_hs'

cd ${DIRECTORY}
scp kartoza5:/home/etienne/healthsites/deployment/script/osm/world.pbf .
# scp hs1-production:/home/web/healthsites/deployment/backups/2017/March/PG_HEALTHSITES_gis.12-March-2017.dmp .
scp hs1-production:/home/web/healthsites/deployment/backups/latest.dmp .


docker run -d -p 5432:5432 --name osm -v /Users/etienne/dev/web/healthsites/deployment/script/osm/:/source kartoza/postgis:9.4-2.1
docker exec -t -i $(PROJECT_ID)-db su - postgres -c "createdb -O docker -T template_postgis gis"
docker exec -t -i $(PROJECT_ID)-db pg_restore /source/latest.dmp | docker exec -i $(PROJECT_ID)-db su - postgres -c "psql gis"
docker exec -it osm su -c "apt-get update"
docker exec -it osm su -c "apt-get install gdal-bin"
docker exec -t osm ogr2ogr -f 'PostgreSQL' PG:"dbname=gis user=docker password=docker host=172.17.0.2" /source/world.pbf --config OSM_CONFIG_FILE /source/osmconf.ini -sql 'SELECT * FROM points WHERE amenity IN ("hospital", "clinic") AND name IS NOT NULL'
docker exec -t osm ogr2ogr -f 'PostgreSQL' PG:"dbname=gis user=docker password=docker host=172.17.0.2" /source/world.pbf --config OSM_CONFIG_FILE /source/osmconf.ini -sql 'SELECT * FROM multipolygons WHERE amenity IN ("hospital", "clinic") AND name IS NOT NULL'
docker kill osm
docker rm osm
