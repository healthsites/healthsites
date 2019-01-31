# -*- coding: utf-8 -*-
"""Settings for when running under docker in development mode."""
import os

from .dev import *  # noqa

print os.environ

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'gis',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'db',
        'PORT': 5432,
        'TEST_NAME': 'unittests',
    },
    'docker_osm': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ['DOCKER_OSM_DATABASE_NAME'],
        'USER': os.environ['DOCKER_OSM_DATABASE_USERNAME'],
        'PASSWORD': os.environ['DOCKER_OSM_DATABASE_PASSWORD'],
        'HOST': os.environ['DOCKER_OSM_DATABASE_HOST'],
        'PORT': os.environ['DOCKER_OSM_DATABASE_PORT'],
        'TEST_NAME': 'docker_osm_unittests',
    }
}
