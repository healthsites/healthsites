#!/bin/bash
export DJANGO_SETTINGS_MODULE=settings.core.dev_${USER}

coverage run manage.py test $@
coverage report
flake8
