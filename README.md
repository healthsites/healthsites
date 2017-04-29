# Welcome to the healthsites code base!

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

Tests status: [![Build Status](https://api.travis-ci.org/healthsites/healthsites.svg)](https://api.travis-ci.org/healthsites/healthsites.svg)

Coverage status: [![Coverage Status](https://coveralls.io/repos/healthsites/healthsites/badge.png?branch=develop)](https://coveralls.io/r/healthsites/healthsites?branch=develop)

Development status: [![Stories in Ready](https://badge.waffle.io/healthsites/healthsites.svg?label=ready&title=Ready)](http://waffle.io/healthsites/healthsites) [![Stories in Ready](https://badge.waffle.io/healthsites/healthsites.svg?label=In%20Progress&title=In%20Progress)](http://waffle.io/healthsites/healthsites)

# License

Data: [Open Database License](http://opendatacommons.org/licenses/odbl/)
Code: [Free BSD License](http://www.freebsd.org/copyright/freebsd-license.html)

Out intention is to foster wide spread usage of the data and the code that we provide. Please use this code and data in the interests of humanity and not for nefarious purposes.

# Setup instructions

**Note** we provide alternative setup instructions for deployment and development under docker - see our [developer documentation](https://github.com/healthsites/healthsites/blob/develop/README-dev.md) for complete details. If you want to develop locally without using docker, follow the steps below.

### Check out the source


First checkout out the source tree:

```
git clone git://github.com/healthsites/healthsites.git
```

Second, go to the source directory:

```
cd django_project
```

### Install

```
make install
```

### Edit the DATABASE section of your Django settings: `dev_${USER}.py`:

```
DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'healthsites_dev',
        'USER': '<your-database-username>',
        'PASSWORD': '<your-password>',
        'HOST': 'localhost',
        # Set to empty string for default.
        'PORT': '5432',
    }
}
```

We assume you have created a postgres database (with postgis extentions) that you can use for your development work. See
[http://postgis.net/install/](http://postgis.net/install/) for details on doing
that.

### Running migrate and collect static

```
make migrate
```

```
make collectstatic
```
