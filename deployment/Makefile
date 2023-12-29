PROJECT_ID := healthsites
export COMPOSE_FILE=docker-compose-osm.yml:docker-compose.yml:docker-compose.override.yml

SHELL := /bin/bash

# ----------------------------------------------------------------------------
#    P R O D U C T I O N     C O M M A N D S
# ----------------------------------------------------------------------------
default: web
run: build web collectstatic

deploy: run
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Bringing up fresh instance "
	@echo "You can access it on http://localhost"
	@echo "------------------------------------------------------------------"

web:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running in production mode"
	@echo "------------------------------------------------------------------"
	@# Dont confuse this with the dbbackup make command below
	@# This one runs the postgis-backup cron container
	@# We add --no-recreate so that it does not destroy & recreate the db container
	@docker-compose up -d

dev:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running in dev mode"
	@echo "------------------------------------------------------------------"
	@docker-compose ${ARGS} --profile dev up -d

build:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Building in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) build --no-cache

nginx:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running nginx in production mode"
	@echo "Normally you should use this only for testing"
	@echo "In a production environment you will typically use nginx running"
	@echo "on the host rather if you have a multi-site host."
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) up -d nginx
	@echo "Site should now be available at http://localhost"

up: web

status:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Show status for all containers"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) ps

kill:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Killing in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) stop

down: kill
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Removing production instance!!! "
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) down

shell:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Shelling in in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) exec django /bin/bash

db-bash:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Entering DB Bash in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) exec db sh

db-shell:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Entering PostgreSQL Shell in production mode"
	@echo "------------------------------------------------------------------"
	docker-compose -p $(PROJECT_ID) exec db su - postgres -c "psql"

collectstatic:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Collecting static in production mode"
	@echo "------------------------------------------------------------------"
	#@docker-compose -p $(PROJECT_ID) run django python manage.py collectstatic --noinput
	#We need to run collect static in the same context as the running
	# django container it seems so I use docker exec here
	# no -it flag so we can run over remote shell
	@docker exec $(PROJECT_ID)_django python manage.py collectstatic --noinput

reload:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Reload django project in production mode"
	@echo "------------------------------------------------------------------"
	# no -it flag so we can run over remote shell
	@docker exec $(PROJECT_ID)_django django --reload  /tmp/django.pid

migrate:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running migrate static in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose exec django python manage.py migrate

# --------------- help --------------------------------

help:
	@echo "* **build** - builds all required containers."
	@echo "* **up** - runs all required containers."
	@echo "* **kill** - kills all running containers. Does not remove them."
	@echo "* **logs** - view the logs of all running containers. Note that you can also view individual logs in the deployment/logs directory."
	@echo "* **nginx** - builds and runs the nginx container."
	@echo "* **permissions** - Update the permissions of shared volumes. Note this will destroy any existing permissions you have in place."
	@echo "* **rm** - remove all containers."
	@echo "* **shell-frontend-mapstore** - open a bash shell in the frontend mapstore (where django runs) container."
