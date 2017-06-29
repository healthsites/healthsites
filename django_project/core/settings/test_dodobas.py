# -*- coding: utf-8 -*-
from .test import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'docker',
        'USER': 'docker',
        'PASSWORD': 'docker',
        'HOST': 'db',
        # Set to empty string for default.
        'PORT': '5432',
    }
}

GDAL_LIBRARY_PATH = '/usr/lib/libgdal.so.20'

GEOS_LIBRARY_PATH = '/usr/lib/libgeos_c.so.1'
