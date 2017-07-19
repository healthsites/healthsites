#!/usr/bin/env bash

ogr2ogr -f 'PostgreSQL' PG:"dbname=gis user=docker password=docker host=172.17.0.2" world.pbf --config OSM_CONFIG_FILE osmconf.ini -sql 'SELECT * FROM points WHERE amenity IN ("hospital", "clinic") AND name IS NOT NULL'
ogr2ogr -f 'PostgreSQL' PG:"dbname=gis user=docker password=docker host=172.17.0.2" world.pbf --config OSM_CONFIG_FILE osmconf.ini -sql 'SELECT * FROM multipolygons WHERE amenity IN ("hospital", "clinic") AND name IS NOT NULL'

On mac :
/usr/local/Cellar/gdal/1.11.5/bin/ogr2ogr -f 'PostgreSQL' PG:"dbname=gis user=docker host=localhost" world.pbf --config OSM_CONFIG_FILE osmconf.ini -sql 'SELECT * FROM points WHERE amenity IN ("hospital", "clinic") AND name IS NOT NULL'
/usr/local/Cellar/gdal/1.11.5/bin/ogr2ogr -f 'PostgreSQL' PG:"dbname=gis user=docker password=docker host=localhost" world.pbf --config OSM_CONFIG_FILE osmconf.ini -sql 'SELECT * FROM multipolygons WHERE amenity IN ("hospital", "clinic") AND name IS NOT NULL'
