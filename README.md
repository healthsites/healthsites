# Welcome to the healthsites code base!

<!-- version 2.0.17 -->

[![Join the chat at https://gitter.im/healthsites/healthsites](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/healthsites/healthsites?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Healthsites is a framework for capturing, publishing and sharing critical
health and sanitation related data to help make these facilities more
accessible and relevant to the communities they serve. Our framework does not
limit our endeavours to these domains and in the future we plan to support
additional domains where it is helpful in humanitarian work.

**Please note that this project is in the early phase of its development.**

You can visit a running instance of healthsites at [healthsites.io](http://healthsites.io).

# Status

These badges reflect the current status of our development branch:

Tests status: [![Build Status](https://travis-ci.org/healthsites/healthsites.svg?branch=develop)](https://travis-ci.org/healthsites/healthsites)

Coverage status: [![Coverage Status](https://coveralls.io/repos/github/healthsites/healthsites/badge.svg?branch=develop)](https://coveralls.io/github/healthsites/healthsites?branch=develop)

Development status: [![Stories in Ready](https://badge.waffle.io/healthsites/healthsites.svg?label=ready&title=Ready)](http://waffle.io/healthsites/healthsites) [![Stories in Ready](https://badge.waffle.io/healthsites/healthsites.svg?label=In%20Progress&title=In%20Progress)](http://waffle.io/healthsites/healthsites)

# License

Data: [Open Database License](http://opendatacommons.org/licenses/odbl/)
Code: [Free BSD License](http://www.freebsd.org/copyright/freebsd-license.html)

Our intention is to foster widespread usage of the data and the code that we provide. Please use this code and data in the interests of humanity and not for nefarious purposes.

# Setup instructions
The Healthsites infrastructure uses Docker with the Django platform, and has two databases. One is a database for use with Django that contains data for all healthsites, another is for the Docker OpenStreetMap database.
Healthsites has a Docker OSM mirror and needs it as main architecture.
To setup the server, please follow the instruction.

### Check out the source


First checkout out the source tree:

```
git clone git://github.com/healthsites/healthsites.git
```

## Production setup

### Just for specific area
If you don't want to specify area instead want to show all of earth data, you can skip this section. 

If you specify the area (like country or continent), you should prepare before deploy:  
1. Prepare the geojson of area first.
2. Search your continent or country in here : http://download.geofabrik.de/. (you can click the continent name to get sub region of it)
3. Right click on *[.osm.pbf]* and copy link 
4. Go to deployment/docker-osm-healthcare/ and change Dockerfile file. Rename https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf in the file into the link that you copied before. 
5. Go to deployment/docker-osm-healthcare/settings and put the geojson area in there and rename it into clip.geojson
6. Preparation is complete, now we need to do next step. 

### How to setup
To start production setup, follow this steps
```
cd healthsites/deployment
make deploy
```

It will run all of architecture automatically. Wait until this error shows: 

```
django.db.utils.ProgrammingError: relation "django_site" does not exist
LINE 1: SELECT (1) AS "a" FROM "django_site" LIMIT 1
```
or

```
django.db.utils.ProgrammingError: relation "osm_healthcare_facilities_node" does not exist
LINE 3: ...sm_id,'-node') as row, 'node' as osm_type, * from osm_health...
```

This is because database in the docker osm needs to be created. 
This database is created automatically by container of docker osm
To fix it, just wait until the container done on creating database by checking it periodically.
To check it
```
docker logs dockerosm_imposm
```
and see if it is creating database in logs like this
```
[Feb 16 09:15:13] [INFO] Imposm took: 1m49.293342244s
Import PBF successful : /home/settings/country.pbf
Installing QGIS styles.
SET
SET
CREATE TABLE
ALTER TABLE
CREATE SEQUENCE

```
The estimation is about >3 hours for earth data.

After it is done, redo
```
cd healthsites/deployment
make deploy
```
and server is ready to be used.
Server can be accessed in
```
http://localhost:49362
```

Healthsites is using cache to fasten the process. To generate this process, some process needs to be done
```
cd healthsites/deployment
make shell
python manage.py generate_cluster_cache
python manage.py generate_countries_cache
```
and wait until everything is done

### Creating admin user
Currently admin can't be accessed because it doesn't had admin user yet.
To do it
```
cd healthsites/deployment
make shell
python manage.py createsuperusr
```
and fill the instruction shows on the terminal

### I have initial database
If we already has initial backups database, we need to restore this database into server.
Put the database into deployment/backups and rename it into latest.dmp

After that, do
```
cd healthsites/deployment
make dbrestore
```

Now, we want to link our data into docker osm data, to do that
```
cd healthsites/deployment
make shell
python manage.py check_localities_osm_id
```
This will taking a lot of time because docker osm is quite a big list.

### Country data extraction
When we access page per country, there will be button to download shapefile.
The generation of shapefile will be done in background for every 24 hours.
But if we want to run it manually, we can do
```
python manage.py generate_shapefile_countries
```

## Development setup
This development setup is just for PyCharm IDE. Please follow this steps.
```
cd healthsites/deployment
make devweb
```
After that, open projects at the pycharm.
Right click `django_project` folder and `Mark Directory as` `Source Root`

### Project settings
Next step is setup our project settings
```
1. Go to File -> settings
2. Go to Project: Healthsites -> Project Interpreter
3. Click `gear` icon and click `SSH Interpreter`
4. Fill host=localhost, username=root and port=49363
5. Next and fill password=docker
6. Next and change interpter to `/usr/bin/python`
7. Change sync folder with remote folder=healthsite folder/django_project and remote folder=/home/web/django_project
8. and click finish
```
### Django settings
Next step is setup our django settings
```
1. Go to File -> settings
2. Go to languages & framework -> django
3. enable `Enable django support`
4. Django project root= locate this (<your healthsites folder>/django_project)
5. settings=core/settings/dev_docker.py
6. Click OK

```

### Run configurations
Now project settings is setup, our next step is setup run configuration to run our development server.
```
1. Go to Run -> Edit Configuration
2. Click + icon and select django server
3. on the right, fill name with anything
4. Host=0.0.0.0
5. Port=8080
6. Python interpreter= Select the one that we create, which has sentences `localhost:49363`
7. Click OK and run!
```

