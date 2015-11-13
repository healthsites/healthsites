
__author__ = 'rischan'

# -*- coding: utf-8 -*-
from .test import *  # noqa

# Temporary hack as travis fails with
# attribute error on ProjectState.render
# whcih is caused by something in localities app
INSTALLED_APPS = tuple(x for x in INSTALLED_APPS if x != 'localities')

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'test_db',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        # Set to empty string for default.
        'PORT': '',
    }
}
