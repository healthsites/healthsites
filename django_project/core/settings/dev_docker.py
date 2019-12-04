# -*- coding: utf-8 -*-
"""Settings for when running under docker in development mode."""
import os

from .dev import *  # noqa

print os.environ

ALLOWED_HOSTS = ['*']

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
        'NAME': 'gis',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'osm-db',
        'PORT': 5432,
        'TEST_NAME': 'docker_osm_unittests',
    }
}

# use master apis for dev
OSM_API_URL = 'https://master.apis.dev.openstreetmap.org'
try:
    SOCIAL_AUTH_OPENSTREETMAP_KEY = SOCIAL_AUTH_OPENSTREETMAP_STAGING_KEY
    SOCIAL_AUTH_OPENSTREETMAP_SECRET = SOCIAL_AUTH_OPENSTREETMAP_STAGING_SECRET
except (ImportError, NameError):
    pass

AUTHENTICATION_BACKENDS = (
    'core.backends.dev_openstreetmap.OpenStreetMapDevOAuth',
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)
