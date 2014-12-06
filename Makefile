SHELL := /bin/bash

default: run

run: build web

deploy: run
	@echo
	@echo "--------------------------"
	@echo "Brining up fresh instance "
	@echo "--------------------------"
	#TODO - replace with something more precise
	@echo "Waiting 20 secs to ensure db is running"
	@sleep 20
	@fig run web python manage.py migrate
	@fig run web python manage.py collectstatic --noinput

rm:
	@echo
	@echo "--------------------------"
	@echo "Killing production instance!!! "
	@echo "--------------------------"
	@fig kill
	@fig rm

web:
	@echo
	@echo "--------------------------"
	@echo "Running in production mode"
	@echo "--------------------------"
	@fig up -d web

build:
	@echo
	@echo "--------------------------"
	@echo "Building in production mode"
	@echo "--------------------------"
	@fig build

migrate:
	@echo
	@echo "--------------------------"
	@echo "Running migrate static in production mode"
	@echo "--------------------------"
	@fig run web python manage.py migrate

collectstatic:
	@echo
	@echo "--------------------------"
	@echo "Collecting static in production mode"
	@echo "--------------------------"
	@fig run web python manage.py collectstatic --noinput

dblogs:
	@echo
	@echo "-----------------------------------"
	@echo "Running db logs in developer mode"
	@echo "press ctrl-c to exit log watcher"
	@echo "-----------------------------------"
	@fig logs db

#
# Staging
#
staging: stagingbuild stagingweb

stagingdeploy: stagingrun
	@echo
	@echo "--------------------------"
	@echo "Bringing up fresh staging instance "
	@echo "--------------------------"
	#TODO - replace with something more precise
	@echo "Waiting 20 secs to ensure db is running"
	@sleep 20
	@fig -f fig-staging.yml run stagingweb python manage.py migrate
	@fig -f fig-staging.yml run stagingweb python manage.py collectstatic --noinput

stagingrm:
	@echo
	@echo "--------------------------"
	@echo "Killing staging instance!!! "
	@echo "--------------------------"
	@fig -f fig-staging.yml kill
	@fig -f fig-staging.yml rm

stagingweb:
	@echo
	@echo "--------------------------"
	@echo "Running in staging mode"
	@echo "--------------------------"
	@fig -f fig-staging.yml up -d stagingweb

stagingbuild:
	@echo
	@echo "--------------------------"
	@echo "Building in staging mode"
	@echo "--------------------------"
	@fig -f fig-staging.yml build

stagingmigrate:
	@echo
	@echo "--------------------------"
	@echo "Running migrate static in staging mode"
	@echo "--------------------------"
	@fig -f fig-staging.yml run stagingweb python manage.py migrate

stagingcollectstatic:
	@echo
	@echo "--------------------------"
	@echo "Collecting static in staging mode"
	@echo "--------------------------"
	@fig -f fig-staging.yml run stagingweb python manage.py collectstatic --noinput



# You need the production mode stuff in place
# before being able to use the dev stuff
# so we call build first
dev: build devssh devmigrate devcollectstatic

devkill:
	@echo
	@echo "-----------------------------------"
	@echo "Killing developer environment"
	@echo "-----------------------------------"
	@fig -f fig-dev.yml kill
	@fig -f fig-dev.yml rm

devdb:
	@echo
	@echo "-----------------------------------"
	@echo "Running db in developer mode"
	@echo "-----------------------------------"
	@fig -f fig-dev.yml up -d --no-recreate devdb

devdblogs:
	@echo
	@echo "-----------------------------------"
	@echo "Running db logs in developer mode"
	@echo "press ctrl-c to exit log watcher"
	@echo "-----------------------------------"
	@fig -f fig-dev.yml logs devdb

devssh:
	@echo
	@echo "--------------------------"
	@echo "Running ssh server in developer mode"
	@echo "You can attach to this as a remote interpreter"
	@echo "in pycharm."
	@echo "--------------------------"
	@fig -f fig-dev.yml up -d --no-recreate dev

devmigrate:
	@echo
	@echo "--------------------------"
	@echo "Migrating in developer mode"
	@echo "--------------------------"
	@fig -f fig-dev.yml run dev /usr/local/bin/ manage.py migrate

devcollectstatic:
	@echo
	@echo "-----------------------------------"
	@echo "Collecting static in developer mode"
	@echo "-----------------------------------"
	@fig -f fig-dev.yml run dev /usr/local/bin/python manage.py collectstatic --noinput

devbuild: build
	@echo
	@echo "--------------------------"
	@echo "Building in developer mode"
	@echo "--------------------------"
	@fig build
	@fig -f fig-dev.yml build

devshell:
	@echo
	@echo "--------------------------"
	@echo "Starting shell in developer mode"
	@echo "--------------------------"
	@echo "Press enter to start your shell"
	@fig -f fig-dev.yml run dev /bin/bash
