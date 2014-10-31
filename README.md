# Welcome to the healthsites code base!

Healthsites is a framework for capturing, publishing and sharing critical
health and sanitation related data to help make these facilities more 
accessible and relevant to the communities they serve. Our framework does not 
limit our endeavours to these domains and in the future we plan to support 
additional domains where it is helpful in humanitarian work.


Tests status: [![Build Status](https://travis-ci.org/konektaz/healthsites.svg)](https://travis-ci.org/konektaz/healthsites)

Coverage status: [![Coverage Status](https://coveralls.io/repos/konektaz/healthsites/badge.png?branch=develop)](https://coveralls.io/r/konektaz/healthsites?branch=develop)

Development status: [![Stories in Ready](https://badge.waffle.io/konektaz/healthsites
.png?label=ready&title=Ready)](https://waffle.io/konektaz/healthsites)




# Setup instructions

```
virtualenv venv
source venv/bin/activate
pip install -r REQUIREMENTS-dev.txt
nodeenv -p --node=0.10.31
npm -g install yuglify
```

# Running collect static

```
virtualenv venv
source venv/bin/activate
cd django_project
python manage.py collectstatic --noinput --settings=core.settings.dev_timlinux
```


# Simple deployment under docker

```

mkdir -p ~/production-sites
cd ~/production-sites
git clone git://github.com/konektaz/healthsites.git


docker run \
    --name="healthsites-postgis" \
    --hostname="healthsites-postgis" \
    -d -t kartoza/postgis
    
docker run \
    --rm \
    --name="healthsites-django" \
    --hostname="healthsites-django" \
    --link healthsites-postgis:healthsites-postgis \
    -v /home/timlinux/production-sites/healthsites:/home/web \
    -p 10080:8000 \
    -i -t ubuntu:trusty /bin/bash

```
   
In the container do:

```
apt-get update
apt-get -y install openssh-server libpq5 python-gdal python-geoip \
    python python-dev python-distribute python-pip python-psycopg2 npm node
npm -g install yuglify
pip install Django==1.7.1 psycopg2 pytz django-braces django-model-utils \
    django-pipeline
```
    
Now in the container run the demo server:

```
export DATABASE_USERNAME=docker
export DATABASE_PASSWORD=docker
export DJANGO_SETTINGS_MODULE=core.settings.prod_docker
export DATABASE_HOST=healthsites-postgis


python manage.py migrate
python manage.py syncdb
python manage.py collectstatic --noinput
python manage.py runserver    


```


