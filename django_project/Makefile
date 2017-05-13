CURRENT_DIR = $(shell pwd)
SETTINGS_DIR = $(CURRENT_DIR)/core/settings

.PHONY: help install_dependencies install delpyc test migrate runserver

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo
	@echo "  install     -- to proceed to a new install of this project. "
	@echo "  delpyc      -- to remove all *.pyc files, this is recursive from the current directory"
	@echo "  migrate    -- to migrate and collectstatic"
	@echo "  runserver   -- to run the Django internal server"
	@echo "  test        -- to run the tests"
	@echo
	@echo

delpyc:
	find . -name "*\.pyc"|xargs rm -f

install_dependencies:
	@echo " Installing dependencies: "
	@echo " "
	sudo apt-get install --quiet --assume-yes python-psycopg2 python-virtualenv

install: install_dependencies
	virtualenv --no-site-packages --setuptools --python python2.7 venv
	venv/bin/pip install -r ../REQUIREMENTS-dev.txt
	venv/bin/nodeenv -p --node=0.10.31
	venv/bin/npm -g install yuglify
	cp $(SETTINGS_DIR)/dev_dodobas.py $(SETTINGS_DIR)/dev_$$USER.py
	@echo " "
	@echo " Now edit dev_$$USER.py setting your database connection details as needed.  "
	@echo " We assume you have created a Postgres database with Postgis extentions for your development work."
	@echo " See http://postgis.net/install/ for details on doing that."
	@echo " "
	@echo " After editing dev_$$USER.py, you can run 'make migrate' to prepare your database."

runserver:
	export RABBITMQ_HOST=localhost; \
	venv/bin/python manage.py runserver --settings=core.settings.dev_${USER}

migrate:
	export RABBITMQ_HOST=localhost; \
	venv/bin/python manage.py migrate --settings=core.settings.dev_${USER}

collectstatic:
	export RABBITMQ_HOST=localhost; \
	venv/bin/python manage.py collectstatic --noinput --settings=core.settings.dev_${USER}
