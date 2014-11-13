# Managing your docker deployed site

This document explains how to do various sysadmin related tasks when your 
site has been deployed under docker.

## Build your docker images and run them

You can simply run the provided script and it will build and deploy the docker
images for you in **production mode**.

``
scripts\create_docker_env.sh
``

To create a test site (or run any of the provided management scripts in test
mode), its the same procedure except you need to export the ``TEST_MODE``
environment variable e.g.::

``
cd healthsites
TEST_MODE=1 scripts\create_docker_env.sh
``

## Setup nginx reverse proxy

You should create a new nginx virtual host - please see 
``*-nginx.conf`` in the root directory of the source for an example.

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

## Management scripts

The following scripts are supplied:

### Create docker env

**Usage example:** ``scripts/create_docker_env.sh``

**Arguments:** None
 
**Description:** Running this script will create the docker images needed to
deploy your application.

![dockerdjangoarchitecture - new page 1](https://cloud.githubusercontent.com/assets/178003/5024388/750b85c8-6b12-11e4-97b0-c73b2d07e539.png)
 
As per the above diagram, it will create the PostGIS and Django docker images.
Depending on the contents of ``scripts/create_docker_env.sh``, additional
images may be created - e.g. a QGIS server image, a QGIS Desktop image (used
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


**Test mode support?:** Yes. See section below on test mode for more details 
prepend the command with TEST_MODE=1 to run on your test site. e.g.

``TEST_MODE=1 scripts/create_docker_env.sh``

When test mode is enabled, a test version of the site architecture will be
created. Typically you will use this when you want to publish 
``test.yoursite.com`` against a development or experimental branch of your 
code that you want to give early adoptors / clients etc. early access to.

In test mode the deployed containers will be named spaced with the prefix
``test-`` in the container names, and the port allocations will be offset
by 100 from the base port of the non test mode services. So for example if
the uwsgi process is running on port 4480 on the production container, the
test uwsgi container will have uwsgi running on port 4580.

**Note:** You can configure the base port used by editing ``scripts/config.sh``.

When deploying under nginx, you should be sure to create a separate virtual
host configuration pointing to the test container's uwsgi port.

An **important note** is that you should deploy the test instance against it's
**own git checkout** otherwise you may encounter unwanted side effects (not
least of all breaking your production site when you check out some experimental
branch).

### Collect static

**Usage example:** ``scripts/collect_static_docker.sh``

**Arguments:** None
 
**Description:** Running this script will create a short lived docker container
based on your production django image. It will mount your code tree under 
``/home/web`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive. It will then run 

```django manage.py collectstatic --noinput --settings=core.settings.prod_docker```

**Test mode support?:** Yes. See section above on **Create docker env** for 
more details prepend the command with TEST_MODE=1 to run on your test site. It 
will then run this command inside the container: e.g.

``TEST_MODE=1 scripts/collect_static_docker.sh``

### Run migrations

**Usage example:** ``scripts/run_migrations_docker.sh``

**Arguments:** None
 
**Description:** Running this script will create a short lived docker container
based on your production django image. It will mount your code tree under 
``/home/web`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive. It will then run this command inside
the container:

```django manage.py migrate --settings=core.settings.prod_docker```

**Test mode support?:** Yes. See section above on **Create docker env** for more 
details prepend the command with TEST_MODE=1 to run on your test site. e.g.

``TEST_MODE=1 scripts/run_migrations_docker.sh``


### Bash prompt

**Usage example:** ``scripts/docker_bash.sh``

**Arguments:** None
 
**Description:** Running this script will create a short lived docker container
based on your production django image. It will mount your code tree under 
``/home/web`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive. It will start an interactive bash
shell inside the container that you can use to run ad hoc commands with 
the django project context and database connection available. 

**Test mode support?:** Yes. See section above on **Create docker env** for more details 
prepend the command with TEST_MODE=1 to run on your test site. e.g.

``TEST_MODE=1 scripts/docker_bash.sh``


### Management commands

**Usage example:** ``scripts/manage.sh``

**Arguments:** Arbitrary django management command options are supported e.g. 

``scripts/manage.sh --help`` 

will invoke the django management command help. There is no need to use the
``--settings`` option unless you want to override it since this option is 
automatically passed in as ``DJANGO_SETTINGS_MODULE=core.settings.prod_docker``.
 
**Description:** Running this script will create a short lived docker container
based on your production django image. It will mount your code tree under 
``/home/web`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive. It will then run this command inside
the container:

```django manage.py <your parameters>```

After running the management command the container will be destroyed.

**Test mode support?:** Yes. See section above on **Create docker env** for more 
details prepend the command with TEST_MODE=1 to run on your test site. e.g.

``TEST_MODE=1 scripts/manage.sh --help``

### Restart django

**Usage example:** ``scripts/restart_django_server.sh``

**Arguments:** None
 
**Description:** Running this script will destroy (if running) the long lived
django uwsgi container, and then restart it. It will mount your code tree under 
``/home/web`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive.

If you need to deploy changes to your django application (e.g. adding some 
new python dependency), the general workflow is:

* rebuild your production image (``cd docker-prod; .build.sh; cd -``)
* restart your production container (``scripts/restart_django_server.sh``)

**Test mode support?:** Yes. See section above on **Create docker env** for more 
details prepend the command with TEST_MODE=1 to run on your test site. e.g.

``TEST_MODE=1 scripts/restart_django_server.sh``

### Run django development server

**Usage example:** ``scripts/run_django_dev_server.sh``

**Arguments:** None
 
**Description:** Running this script will destroy (if running) the long lived
django development container, and then restart it. It will mount your code tree under 
``/home/web`` via a docker shared volume and create a link to your database
container, using docker's ``--link`` directive.

If you need to deploy changes to your django application (e.g. adding some 
new python dependency), the general workflow is:

* rebuild your development image (``cd docker-dev; .build.sh; cd -``)
* restart your development container (``scripts/run_django_dev_server.sh``)

When the development container starts, it will launch sshd which you can connect
to using the credentials:

* **User:** docker
* **Password:** docker

Please see README-dev.md for more details on how to use this development
container for efficient development from within PyCharm.

**Test mode support?:** No

``TEST_MODE=1 scripts/restart_django_server.sh``

### Run QGIS desktop

**Usage example:** ``scripts/run_qgis_desktop.sh``

**Arguments:** None
 
**Description:** Running this script will destroy (if running) the long lived
QGIS desktop container, and then restart it. It will mount your the ``webmaps``
directory from in your code tree under ``/web`` in the container via a docker 
shared volume and create a link to your database, using docker's ``--link`` 
directive.


**Test mode support?:** Currently unsupported! The main issue is that
QGIS project files cannot honour the environmentals which are used to 
define the PostgreSQL connection details. So our recommendation is that you
run a copy of the production mode environment on your local machine when you
are building out QGIS projects against the docker service.


# Configuration options

You can configure the base port used and various other options like the
image organisation namespace and postgis user/pass by editing 
``scripts/config.sh``.
