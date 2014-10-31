# Welcome to the healthsites code base!

Healthsites is a framework for capturing, publishing and sharing critical
health and sanitation related data to help make these facilities more 
accessible and relevant to the communities they serve. Our framework does not 
limit our endeavours to these domains and in the future we plan to support 
additional domains where it is helpful in humanitarian work.


Tests status: [![Build Status](https://travis-ci.org/konektaz/healthsites.svg)](https://travis-ci.org/konektaz/healthsites)

Coverage status: [![Coverage Status](https://coveralls.io/repos/konektaz/healthsites/badge.png?branch=develop)](https://coveralls.io/r/konektaz/healthsites?branch=develop)

Development status: [![Stories in Ready](https://badge.waffle.io/konektaz/healthsites.svg?label=ready&title=Ready)](http://waffle.io/konektaz/healthsites) [![Stories in Ready](https://badge.waffle.io/konektaz/healthsites.svg?label=In%20Progress&title=In%20Progress)](http://waffle.io/konektaz/healthsites)




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
mkdir /tmp/healthsites-tmp
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
    -e DATABASE_NAME=gis \
    -e DATABASE_USERNAME=docker \
    -e DATABASE_PASSWORD=docker \
    -e DATABASE_HOST=healthsites-postgis \
    --link healthsites-postgis:healthsites-postgis \
    -v /home/${USER}/production-sites/healthsites:/home/web \
    -v /tmp/healthsites-tmp:/tmp/healthsites-tmp \
    -p 49360:49360 \
    -i -t konektaz/healthsites

```
   
In the container do:

```

```
    
Now in the container run the demo server:

```
export DATABASE_NAME=gis
export DATABASE_USERNAME=docker
export DATABASE_PASSWORD=docker
export DATABASE_HOST=healthsites-postgis
export DJANGO_SETTINGS_MODULE=core.settings.prod_docker

python manage.py migrate
python manage.py collectstatic --noinput
python manage.py runserver    
```


