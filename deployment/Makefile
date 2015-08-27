SHELL := /bin/bash
PROJECT_ID := healthsites

# ----------------------------------------------------------------------------
#    P R O D U C T I O N     C O M M A N D S
# ----------------------------------------------------------------------------

default: web

run: build web

deploy: run migrate collectstatic
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Bringing up fresh instance "
	@echo "You can access it on http://localhost:49361"
	@echo "------------------------------------------------------------------"

build:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Building in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) build

web:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) up -d web
	@docker-compose -p $(PROJECT_ID) up --no-recreate -d dbbackups

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

migrate:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running migrate static in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py migrate

collectstatic:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Collecting static in production mode"
	@echo "------------------------------------------------------------------"
	#@docker-compose -p $(PROJECT_ID) run uwsgi python manage.py collectstatic --noinput
	#We need to run collect static in the same context as the running
	# uwsgi container it seems so I use docker exec here
	@docker exec -t -i $(PROJECT_ID)_uwsgi_1 python manage.py collectstatic --noinput

reload:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Reload django project in production mode"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)_uwsgi_1 uwsgi --reload  /tmp/django.pid

worker:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running worker in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run worker

kill:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Killing in production mode"
	@echo "------------------------------------------------------------------"

	@docker-compose -p $(PROJECT_ID) kill

rm: kill
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Removing production instance!!! "
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) rm

logs:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Showing uwsgi logs in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) logs uwsgi

workerlogs:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Showing celery worker logs in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) logs worker

dblogs:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Showing db logs in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) logs db

nginxlogs:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Showing nginx logs in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) logs web

shell:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Shelling in in production mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID) run uwsgi /bin/bash

dbshell:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Shelling in in production database"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)_db_1 psql -U docker -h localhost gis

sentry:
	@echo
	@echo "--------------------------"
	@echo "Running sentry production mode"
	@echo "--------------------------"
	@docker-compose  -p $(PROJECT_ID) up -d sentry

maillogs:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Showing smtp logs in production mode"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)_smtp_1 tail -f /var/log/mail.log

mailerrorlogs:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Showing smtp error logs in production mode"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)_smtp_1 tail -f /var/log/mail.err

mapproxylogs:
	@echo
	@echo "--------------------------"
	@echo "Showing mapproxy logs in production mode"
	@echo "--------------------------"
	@docker-compose -p $(PROJECT_ID) logs mapproxy

seed:
	@echo
	@echo "--------------------------"
	@echo "Seeding mapproxy in production mode"
	@echo "--------------------------"
	@docker-compose -p $(PROJECT_ID) run mapproxy /usr/local/bin/mapproxy-seed -f /mapproxy/mapproxy.yaml /mapproxy/seed.yaml

map:
	@echo
	@echo "--------------------------"
	@echo "Getting current 6 hour slot as pdf map"
	@echo "Make sure you have started the services with make run first"
	@echo "--------------------------"
	# Experimental way we had of getting it using QGIS Server
	#wget -O map.pdf "http://172.17.0.6/cgi-bin/qgis_mapserv.fcgi?map=/web/jk-floods.qgs&SERVICE=wms&LAYERS=Rw&REQUEST=GetPrint&TEMPLATE=6Hour&map0:EXTENT=11862318.594,-714081.378,11922154.957,-675870.096&map0:ROTATION=0&FORMAT=pdf&DPI=300"
	docker exec -t -i $(PROJECT_ID)_cron_1 xvfb-run python /home/web/cron-scripts/pdf_report_generator.py
	@echo "--------------------------"
	@echo "PDF Generated - written to reports"
	@echo "--------------------------"
	evince reports/jk-floods-latest.pdf

qgis:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running QGIS desktop in production mode"
	@echo "Make sure you have started the services with make run first"
	@echo "------------------------------------------------------------------"
	@xhost +; docker run --rm --name="qgis-desktop-2-8" \
	-i -t \
	--link $(PROJECT_ID)_db_1:db \
	--link $(PROJECT_ID)_qgisserver_1:qgisserver \
	--link $(PROJECT_ID)_mapproxy_1:mapproxy \
	--volumes-from $(PROJECT_ID)_qgisserver_1 \
	-v ${HOME}:/home/$(USER) \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-e DISPLAY=unix$(DISPLAY) \
	kartoza/qgis-desktop:2.8.0; xhost -



# ----------------------------------------------------------------------------
#    S T A G I N G     C O M M A N D S
# ----------------------------------------------------------------------------

staging-run: staging-build staging-web

staging-deploy: staging-run staging-migrate staging-collectstatic
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Bringing up fresh staging instance "
	@echo "You can access it on http://localhost:49362"
	@echo "------------------------------------------------------------------"

staging-build:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Building in staging mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID)-staging build

staging-web:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running in staging mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID)-staging up -d stagingweb

staging-migrate:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running migrate static in staging mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID)-staging run uwsgi python manage.py migrate

staging-collectstatic:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Collecting static in staging mode"
	@echo "------------------------------------------------------------------"
	#@docker-compose -p $(PROJECT_ID)-staging run uwsgi python manage.py collectstatic --noinput
	#We need to run collect static in the same context as the running
	# uwsgi container it seems so I use docker exec here
	@docker exec -t -i $(PROJECT_ID)staging_uwsgi_1 python manage.py collectstatic --noinput

staging-reload:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Reload django project in staging mode"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)staging_uwsgi_1 uwsgi --reload /tmp/django.pid

staging-kill:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Killing in staging mode"
	@echo "------------------------------------------------------------------"

	@docker-compose -p $(PROJECT_ID)-staging kill

staging-worker:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running worker in staging mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID)-staging run worker

staging-rm: kill
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Removing staging instance!!! "
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID)-staging rm

staging-logs:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Showing uwsgi logs in staging mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID)-staging logs uwsgi

staging-nginxlogs:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Showing nginx logs in staging mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID)-staging logs web

staging-shell:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Shelling in in staging mode"
	@echo "------------------------------------------------------------------"
	@docker-compose -p $(PROJECT_ID)-staging run uwsgi /bin/bash

staging-dbshell:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Shelling in in staging database"
	@echo "------------------------------------------------------------------"
	@docker exec -t -i $(PROJECT_ID)staging_db_1 psql -U docker -h localhost gis

staging-qgis:
	@echo
	@echo "------------------------------------------------------------------"
	@echo "Running QGIS desktop in staging mode"
	@echo "Make sure you have started the services with make run first"
	@echo "------------------------------------------------------------------"
	@xhost +; docker run --rm --name="qgis-desktop-2-8.0" \
	-i -t \
	--link $(PROJECT_ID)staging_db_1:db \
	--link $(PROJECT_ID)staging_qgisserver_1:qgisserver \
	--volumes-from $(PROJECT_ID)_qgisserver_1 \
	-v ${HOME}:/home/$(USER) \
	-v /tmp/.X11-unix:/tmp/.X11-unix \
	-e DISPLAY=unix$(DISPLAY) \
	kartoza/qgis-desktop:2.8; xhost -
