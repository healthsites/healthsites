# Welcome to the healthsites code base!

[![Join the chat at https://gitter.im/konektaz/healthsites](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/konektaz/healthsites?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![Join the chat at https://gitter.im/konektaz/healthsites](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/konektaz/healthsites?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Healthsites is a framework for capturing, publishing and sharing critical
health and sanitation related data to help make these facilities more 
accessible and relevant to the communities they serve. Our framework does not 
limit our endeavours to these domains and in the future we plan to support 
additional domains where it is helpful in humanitarian work.

**Please note that this project is in the early phase of its development.**

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

**Note** we provide alternative setup instructions for deployment and development under docker - see our [developer documentation](https://github.com/konektaz/healthsites/blob/develop/README-dev.md) for complete details. If you want to develop locally without using docker, follow the steps below.

### Check out the source


First checkout out the source tree:

```
git clone git://github.com/konektaz/healthsites.git
```

### Install dependencies

```
sudo apt-get install python-psycopg2 python-virtualenv
```

```
cd healthsites
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




