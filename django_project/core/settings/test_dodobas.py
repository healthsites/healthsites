# -*- coding: utf-8 -*-
from .test import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'healthsites_dev',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'postgresql',
        # Set to empty string for default.
        'PORT': '5433',
    }
}
