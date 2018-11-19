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
    }
}
