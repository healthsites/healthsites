# Managing your docker deployed site

**Note:** This documentation is intentionally generic so that it can
be copy-pasted between projects - do not put project specific details here.

This document explains how to do various sysadmin related tasks when your
site has been deployed under docker. Three deployment modes are supported:

* **production**: no debug etc is enabled, has its own discrete database. Configure
  your production environment in core.settings.prod_docker - this
  DJANGO_SETTINGS_MODULE is used when running in production mode.
* **staging**: Configure your staging environment in core.settings.staging_docker -
  this DJANGO_SETTINGS_MODULE is used when running in production mode.
* **development**: Configure your development environment in core.settings.dev_docker -
  this DJANGO_SETTINGS_MODULE is used when running in production mode. Please see
  README-dev.md for more information on setting up a developer environment.

**Note:** We really recommend that you use docker 1.3 or great so that you
  can take advantage of the exec command as well as other newer features.

## Build your docker images and run them

### Production

You can simply run the provided script and it will build and deploy the docker
images for you in **production mode**.

```
fig build
fig up -d web
fig run web python manage.py migrate
fig run web python manage.py collectstatic --noinput
```

Alternatively you can use make commands if your OS has Gnu Make installed:

```
make deploy
```

#### Using make

Using the make commands is probably simpler - the following make commands are
provided for production:


* **run** - builds then runs db and uwsgi services
* **web** - run django uwsgi instance (will bring up db too if needed)
* **collectstatic** - collect static in production instance
* **migrate** - run django migrations in production instance
* **build** - build production containers
* **deploy** - run db, web, wait 20 seconds, collect static and do migrations
* **rm** - completely remove staging from your system (use with caution)

e.g. ``make web``

#### Arbitrary commands

Running arbitrary management commands is easy (assuming you have docker >= 1.3)
e.g.:

```
docker exec foo_web_1 /usr/local/bin/python /home/web/django_project/manage.py --help
```

**Note:** rm should not destroy any data since it only removes containers
and not host volumes for db and django. All commands should be non-destructive
to existing data - though **smart people make backups before changing things**.


### Staging

**Please use a separate git checkout for your staging database!**

#### Using fig

To create a staging site (or run any of the provided management scripts in
staging mode), its the same procedure except you need to use the
``fig-staging.yml`` environment variable e.g.::

``
fig -f fig-staging.yml build
fig -f fig-staging.yml up -d stagingweb
fig -f fig-staging.yml run stagingcollectstatic
fig -f fig-staging.yml run stagingmigrate
``

#### Using make

Using the make commands is probably simpler - the following make commands are
provided for staging:


* **staging** - setup and run the staging web service
* **stagingcollectstatic**  - collect static in staging instance
* **stagingmigrate** - run django migrations in staging instance
* **stagingweb** - run django uwsgi instance (will bring up db too if needed)
* **stagingbuild** - build staging containers
* **stagingdeploy** - run db, web, wait 20 seconds, collect static and do migrations
* **stagingrm** - completely remove staging from your system (use with caution)


**Note:** stagingrm should not destroy any data since it only removes containers
and not host volumes for db and django.

#### Arbitrary commands

Running arbitrary management commands is easy (assuming you have docker >= 1.3)
e.g.:

```
docker exec foo_stagingweb_1 /usr/local/bin/python /home/web/django_project/manage.py --help
```

## Setup nginx reverse proxy

You should create a new nginx virtual host - please see
``*-nginx.conf`` in the root directory of the source for an example. There is
one provided for production and one for staging.

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


### Managing containers

Please refer to the general [fig documentation](http://www.fig.sh/cli.hyml)
for further notes on how to manage the infrastructure using fig.

# Configuration options

You can configure the base port used and various other options like the
image organisation namespace and postgis user/pass by editing the ``fig*.yml``
files.
