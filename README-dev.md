# Setup pycharm to work with a remove docker development environment

## Build your dev docker image

This image extents the production one, adding ssh to it. You must
have built the production one first!

```
cd docker-dev
./build.sh
```

## Run the dev container

We provide a script to start the container:

```
scripts/run_django_dev_server.sh
```

Which should produce output like this:

```
Running django development server with option
Access it via ssh on port 1122 of your host
Use these connection details:

  user: docker
  password: docker

to log into the container via ssh or when setting up your
pycharm remote python environment.

Access it via http on port 1180 of your host
after starting the dev server like this:

python manage.py runserver 0.0.0.0:1180
------------------------------------------

```

## Create a remote interpreter in pycharm

Open the project in pycharm then do:

* File -> Settings
* Project Interpreter
* Click on the gear icon next to project interpreter
* Add remote...

Now use these credentials:

* SSH Credentials (tick)
* Host: localhost
* Port: 1122 (or whatever the instructions above give as the ssh port)
* User name: docker
* Auth type: password (and tick 'save password')
* Password: docker
* Python interpreter path: /usr/bin/python

When prompted about host authenticity, click Yes

In settings, django support:

* tick to enable django support.
* Set django project root to the path on your host that holds django code e.g. ``/home/timlinux/dev/python/healthsites/django_project``
* Set the settings option to your setting profile e.g. ``core/settings/dev_timlinux.py``
* manage script (leave default)


## Create the django run configuration

* Run -> Edit configurations
* Click the green + icon in the top left corner
* Choose ``Django server`` from the popup list

Now set these options:

* Name: Django Server
* Host: 0.0.0.0
* Port: 1180 (or whatever is defined in the docker run output above)
* Additional options: ``--settings=core.settings.dev_timlinux`` (replace with your dev_ file as needed)
* Environment vars: Leave as default unless you need to add something to the env
* Python interpreter: Ensure it is set you your remote interpreter (should be set to that by default)
* Interpreter options: Leave blank
* Path mappings: Here you need to indicate path equivalency between your host filesystem and the filesystem in the remote (docker) host. Click the ellipsis and add a run that points to your git checkout on your local host and the /home/web directory in the docker host. e.g.
  * Local path: /home/timlinux/dev/python/healthsites
  * Remote path: /home/web
* click OK to save your run configuration

Now you can run the server using the green triangle next to the Django server label in the run configurations pull down. Debug will aslo work and you will be able to step through views etc as you work.



