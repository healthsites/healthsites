# Welcome to the healthsites code base!

Healthsites is a framework for capturing, publishing and sharing critical
health and sanitation related data to help make these facilities more 
accessible and relevant to the communities they serve. Our framework does not 
limit our endeavours to these domains and in the future we plan to support 
additional domains where it is helpful in humanitarian work.

You can visit a running instance of healthsites at [healthsites.io](http://healthsites.io).

# Status

These badges reflect the current status of our development branch:

Tests status: [![Build Status](https://travis-ci.org/konektaz/healthsites.svg)](https://travis-ci.org/konektaz/healthsites)

Coverage status: [![Coverage Status](https://coveralls.io/repos/konektaz/healthsites/badge.png?branch=develop)](https://coveralls.io/r/konektaz/healthsites?branch=develop)

Development status: [![Stories in Ready](https://badge.waffle.io/konektaz/healthsites.svg?label=ready&title=Ready)](http://waffle.io/konektaz/healthsites) [![Stories in Ready](https://badge.waffle.io/konektaz/healthsites.svg?label=In%20Progress&title=In%20Progress)](http://waffle.io/konektaz/healthsites)

# License

Data: [Open Database License](http://opendatacommons.org/licenses/odbl/)
Code: [Free BSD License](http://www.freebsd.org/copyright/freebsd-license.html)

Out intention is to foster wide spread usage of the data and the code that we provide. Please use this code and data in the interests of humanity and not for nefarious purposes.

# Setup instructions

## Simple deployment under docker

### Overview

You need two docker containers:

* A postgis container
* A uwsgi container

We assume you are running nginx on the host and we will set up a reverse
proxy to pass django requests into the uwsgi container. Static files will
be served directly using nginx on the host.

A convenience script is provided under ``scripts\create_docker_env.sh`` which
should get everything set up for you. Note you need at least docker 1.2 - use
the [installation notes](http://docs.docker.com/installation/ubuntulinux/) 
on the official docker page to get it set up.

### Check out the source


First checkout out the source tree:

```
mkdir -p ~/production-sites
mkdir /tmp/healthsites-tmp
cd ~/production-sites
git clone git://github.com/konektaz/healthsites.git
```

### Build your docker images and run them

You can simply run the provided script and it will build and deploy the docker
images for you.

``
cd healthsites
scripts\create_docker_env.sh
``

### Setup nginx reverse proxy

You should create a new nginx virtual host - please see 
``healthsites-nginx.conf`` in the root directory of the source for an example.


## For local development

### Install dependencies

```
virtualenv venv
source venv/bin/activate
pip install -r REQUIREMENTS-dev.txt
nodeenv -p --node=0.10.31
npm -g install yuglify
```

### Create your dev profile



```
cd django_project/core/settings
cp dev_dodobas.py dev_${USER}.py
```

Now edit dev_<your username> setting your database connection details as
needed. We assume you have created a postgres (with postgis extentions) 
database somewhere that you can use for your development work. See 
[http://postgis.net/install/](http://postgis.net/install/) for details on doing
that.

### Running collect and migrate static

Prepare your database and static resources by doing this:

```
virtualenv venv
source venv/bin/activate
cd django_project
python manage.py migrate
python manage.py collectstatic --noinput --settings=core.settings.dev_${USER}
```




