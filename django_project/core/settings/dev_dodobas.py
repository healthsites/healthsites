# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join, pardir

from .dev import *  # noqa

PROJECT_PATH = abspath(join(dirname(__file__), pardir, pardir))
MEDIA_ROOT = join(PROJECT_PATH, 'media')
STATIC_ROOT = join(PROJECT_PATH, 'static')

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'hs_dev',
        'USER': '',
        'PASSWORD': '',
        'HOST': 'postgresql',
        # Set to empty string for default.
        'PORT': '5433',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # define output formats
        'verbose': {
            'format': (
                '%(levelname)s %(name)s %(asctime)s %(module)s %(process)d '
                '%(thread)d %(message)s')
        },
        'simple': {
            'format': (
                '%(name)s %(levelname)s %(filename)s L%(lineno)s: '
                '%(message)s')
        },
    },
    'handlers': {
        # console output
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
        },
        # 'logfile': {
        #     'class': 'logging.FileHandler',
        #     'filename': '/tmp/app-dev.log',
        #     'formatter': 'simple',
        #     'level': 'DEBUG',
        # }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'INFO',  # switch to DEBUG to show actual SQL
        },
        # example app logger
        'localities': {
            'level': 'INFO',
            'handlers': ['console'],
            # propagate is True by default, which proppagates logs upstream
            'propagate': False
        }
    },
    # root logger
    # non handled logs will propagate to the root logger
    'root': {
        'handlers': ['console'],
        'level': 'WARNING'
    }
}
