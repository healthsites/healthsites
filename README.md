# Welcome to the healthsites code base!

<!-- version 3.0.1 -->

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

Development status: [User stories in the backlog](https://github.com/healthsites/healthsites/projects/12)

# License

Data: [Open Database License](http://opendatacommons.org/licenses/odbl/)<br>
Data credits : &copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors <br>
Code: [3-clause BSD License](https://opensource.org/license/bsd-3-clause/)

Our intention is to foster widespread usage of the data and the code that we provide. Please use this code and data in the interests of humanity and not for nefarious purposes.

# Setup instructions

1. Copy the `.env` template to project root

```shell
cp deployment/.template.env .env
```

2. Copy docker-compose file

```shell
cp deployment/docker-compose.override.template.yml deployment/docker-compose.override.yml
```

3. Change the PBF file to smaller one, i.e. from Senegal

```Dockerfile
# change this
RUN wget https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf  -O settings/country.pbf
# to this
RUN wget https://download.geofabrik.de/africa/senegal-and-gambia-latest.osm.pbf -O settings/country.pbf
```

4. Run `make`

Additional steps:

1. Because the imposm may fail as the database container is not ready, you may need to restart it.

```shell
docker restart healthsites_osm_imposm
```
