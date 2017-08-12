# healthsites.io: a free, curated, canonical source of healthcare location data

[![Join the chat at https://gitter.im/healthsites/healthsites](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/healthsites/healthsites)

Healthsites is a framework for capturing, publishing and sharing critical
health and sanitation related data to help make these facilities more
accessible and relevant to the communities they serve. Our framework does not
limit our endeavours to these domains and in the future we plan to support
additional domains where it is helpful in humanitarian work.

**Please note that this project is in the early phase of its development.**

You can visit a running instance of healthsites at [healthsites.io](http://healthsites.io).

# Status

These badges reflect the current development status of the project:

Tests status: [![Build Status](https://travis-ci.org/healthsites/healthsites.svg?branch=develop)](https://travis-ci.org/healthsites/healthsites)

Coverage status: [![Coverage Status](https://coveralls.io/repos/github/healthsites/healthsites/badge.svg?branch=master)](https://coveralls.io/github/healthsites/healthsites?branch=master)

Development status: [![Stories in Ready](https://badge.waffle.io/healthsites/healthsites.svg?label=ready&title=Ready)](http://waffle.io/healthsites/healthsites) [![Stories in Ready](https://badge.waffle.io/healthsites/healthsites.svg?label=In%20Progress&title=In%20Progress)](http://waffle.io/healthsites/healthsites)

# License

Data: [Open Database License](http://opendatacommons.org/licenses/odbl/)

Code: [Free BSD License](http://www.freebsd.org/copyright/freebsd-license.html)

Out intention is to foster wide spread usage of the data and the code that we
provide. Please use this code and data in the interests of humanity and not
for nefarious purposes.

# Getting started


The quickest way to get started with the Healthsites project is using [docker-compose](https://docs.docker.com/compose/).


```
docker-compose build

docker-compose up -d

docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py createsuperuser
```
