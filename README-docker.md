# Managing your docker deployed site

This document explains how to do various sysadmin related tasks when your 
site has been deployed under docker. The docker deployed version of this
application is managed from the ``deployment`` directory using either
``docker-compose`` or (for your convenience) ``make`` commands. Please 
ensure that you have both ``docker`` and ``docker-compose`` installed
before commencing with these instructions (see [docker installation docs
for details](https://docs.docker.com/installation/)).


# Management scripts

The following scripts are supplied:

## Create docker env

**Usage example:** ``make run``
 
**Description:** Running this script will create the docker containers needed to
deploy your application.

![dockerdjangoarchitecture - new page 1](https://cloud.githubusercontent.com/assets/178003/5024388/750b85c8-6b12-11e4-97b0-c73b2d07e539.png)
 
As per the above diagram, it will create the PostGIS and Django docker containers.
Depending on the contents of ``docker-compose.yml``, additional
containers may be created - e.g. a QGIS server image, a QGIS Desktop image (used
for creating maps within the production environment context) and so on.

After creating the images (or fetching them if they are being used from 
the docker hub repository), container instances will be deployed and
initialisation will be carried out (e.g. migrations, collect statict) - 
please see the source of the create_docker_env.sh script to see exactly
which steps are carried out.

Once the command is run, you should see a number of docker containers running
and linking to each other when you run the ``docker ps`` command. You 
should also be able to visit the site in your web browser after ensuring that
your nginx proxy configuration is correct.

When building out the infrastructure, sequential port numbers will be allocated
to the various services defined in the containers. Again these can be viewed
using the ``docker ps`` command.



## Collect static

**Usage example:** ``make collectstatic``
 
**Description:** Running this script will create a short lived docker container
based on your production django image. It will mount your ``django_project`` as 
``/home/web/django_project`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive. It will then run:

```django manage.py collectstatic --noinput --settings=core.settings.prod_docker```

## Run migrations

**Usage example:** ``make migrations``

**Description:** Running this script will create a short lived docker container
based on your production django image. It will mount your ``django_project`` as 
``/home/web/django_project`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive. It will then run:


```django manage.py migrate --settings=core.settings.prod_docker```


## Bash prompt

**Usage example:** ``make shell``

**Description:** Running this script will create a short lived docker container
based on your production django image.  It will mount your ``django_project`` as 
``/home/web/django_project`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive. It will start an interactive bash
shell inside the container that you can use to run ad hoc commands with 
the django project context and database connection available. 


## Restart django

**Usage example:** ``make reload``

**Description:** Running this script will reload the uwsgi process in the 
django uwsgi container, and then restart it. It will mount your ``django_project`` as 
``/home/web/django_project`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive.


# Configuration options

You can configure the base port used and various other options like the
image organisation namespace and postgis user/pass by editing 
``docker-compose.yml``.

# Setup nginx reverse proxy

You should create a new nginx virtual host - please see 
``*-nginx.conf`` in the ``deployment`` directory of the source for an example.

Simply add the example file to your ``/etc/nginx/sites-enabled/`` directory 
and then modify the contents to match your local filesystem paths. Then use

```
sudo nginx -t
```

To verify that your configuration is correct and then reload / restart nginx
e.g.

```
sudo /etc/init.d/nginx restart
```
