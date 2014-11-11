#!/bin/bash
export DJANGO_SETTINGS_MODULE=core.settings.test_${USER}

coverage run manage.py test $@

echo "##############"
echo "#  Coverage  #"
echo "##############"
coverage report

echo "############"
echo "#  Flake8  #"
echo "############"
flake8
