# Welcome to the healthsites code base!

<!-- version 3.0.1 -->

[![Join the chat at https://gitter.im/healthsites/healthsites](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/healthsites/healthsites?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Healthsites is a framework for capturing, publishing and sharing critical
health and sanitation related data to help make these facilities more
accessible and relevant to the communities they serve. Our framework does not
limit our endeavours to these domains and in the future we plan to support
additional domains where it is helpful in humanitarian work.

**Please note that this project is in the early phase of its development.**

You can visit a running instance of healthsites
at [healthsites.io](http://healthsites.io).

# Status

These badges reflect the current status of our development branch:

Tests
status: [![Build Status](https://travis-ci.org/healthsites/healthsites.svg?branch=develop)](https://travis-ci.org/healthsites/healthsites)

Coverage
status: [![Coverage Status](https://coveralls.io/repos/github/healthsites/healthsites/badge.svg?branch=develop)](https://coveralls.io/github/healthsites/healthsites?branch=develop)

Development
status: [User stories in the backlog](https://github.com/healthsites/healthsites/projects/12)

# License

Data: [Open Database License](http://opendatacommons.org/licenses/odbl/)<br>
Data credits : &copy; <a href="http://www.openstreetmap.org/copyright">
OpenStreetMap</a> contributors <br>
Code: [3-clause BSD License](https://opensource.org/license/bsd-3-clause/)

Our intention is to foster widespread usage of the data and the code that we
provide. Please use this code and data in the interests of humanity and not for
nefarious purposes.

# Setup instructions

## Prerequisites

### Docker

We recommend using the official Docker packages (not those provided by your
distro) and assume membership of the docker group.
See [docker.io's](https://docs.docker.com/engine/install/ubuntu/) guide for
setup notes and below for adding yourself to the docker group.

```
sudo usermod -a -G docker $user
```

(Restart your computer after making this change)

### Docker-compose

You need to have docker-compose installed - version 1.29 or later should work
fine.

### Git

You should have [Git](You should have Git installed.) installed.

### Make

```
sudo apt install make
```

## Cloning

Ananymous Git code check out https://github.com/healthsites/healthsites.git

```
git clone https://github.com/healthsites/healthsites.git
```

Alternatively check out over ssh:

```
git clone git@github.com:healthsites/healthsites.git
```

## Deployment Guide

### Copy the Environment Configuration

Copy the **.env.template** to the project root directory:

```shell
cp deployment/.template.env .env
```

### Copy the Docker Compose Configuration

Copy the **docker-compose** override file:

```shell
cp deployment/docker-compose.override.template.yml deployment/docker-compose.override.yml
```

### Update the PBF File for a Specific Country

Since the global PBF file is significantly large, it is recommended to use a
country-specific PBF file. For example, to use the South Africa PBF file,
follow these steps:

Navigate to the deployment/docker-osm-profile directory.
Open the Dockerfile in a text editor.

Modify line 11 as follows:

**Before:**

```
RUN wget https://planet.openstreetmap.org/pbf/planet-latest.osm.pbf  -O settings/country.pbf
```

**After:**

```
RUN wget https://download.geofabrik.de/africa/south-africa-latest.osm.pbf -O settings/country.pbf
```

For additional country-specific PBF files, refer
to [Geofabrik’s download page](https://download.geofabrik.de/) and copy the
relevant .osm.pbf link.

### Start the Development Environment

Run the following command and wait until the process completes:

```
make dev
```

And wait until it is done.

### Verify Deployment Completion and Prepare Data

Next setup is preparing our data and cache

Run the following command:
```
docker logs -f healthsites_osm_osmenrich
```

Wait the process until it says

```
Sleeping for 120 seconds.
```

The waiting estimation for South Africa data is around 20 minutes, depend on the internet speed.

Once this message appears, do **ctrl+c** 
And execute the following commands to prepare the data and generate the cache:
```
make prepare-data
make generate-cache
```

### Verify the development server

During the initial deployment, the development server will be unavailable because the database is not yet ready.

To ensure the development server is operational, run the following command:
```
docker restart healthsites_dev
```

### Accessing the Website

After the deployment is complete, you can access the application via:

- Production server: http://localhost/
- Development server: http://localhost:2000/

**Difference Between Production and Development:**

In the development environment, changes to the code will take effect immediately upon refreshing the browser.

### Additional steps:

Because the imposm may fail as the database container is not ready, you may
need to restart it.

```shell
docker restart healthsites_osm_imposm
```


### Restarting the Development Server
If you need to turn off your machine and back to your machine, simply restart the development server by running:
```
make dev
```
This will restore access to the website without requiring previous preparation steps.
