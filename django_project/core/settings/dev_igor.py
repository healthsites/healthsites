# -*- coding: utf-8 -*-
import os
from .dev import *  # noqa

DATABASES = {
    'default': {
        # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        # Or path to database file if using sqlite3.
        'NAME': 'cit_dev',
        # The following settings are not used with sqlite3:
        'USER': 'cit',
        'PASSWORD': 'cit',
        # Empty for localhost through domain sockets or '127.0.0.1' for
        # localhost through TCP.
        'HOST': os.environ['DBCONTAINERH_IP'],
        # Set to empty string for default.
        'PORT': '5432',
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
            'level': 'DEBUG',
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

SOCIAL_AUTH_OPENSTREETMAP_KEY = 'jDdNNwcqojKUcGVNxXSlpKwTi6q1LH24rKxUHnoY'
SOCIAL_AUTH_OPENSTREETMAP_SECRET = 'AS2nYDWEryS0H2mPS7gHqW2dCnAJyUYOghWUWCDu'

SOCIAL_AUTH_TWITTER_KEY = 'fMUAWDOUFR7Bj18yArV5xFtGA'
SOCIAL_AUTH_TWITTER_SECRET = 'qWpWIpYUBpN73WbwZYF25p2quHleHwNxmZ5Ss1Y7ryzqYtviwC'

SOCIAL_AUTH_GITHUB_KEY = '80bd823edf9b37bc1faa'
SOCIAL_AUTH_GITHUB_SECRET = '5044e80411289a89bcfc41dd30c70cb2abd9917a'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '118859538322-cvdq0g5pev88oigsjmpvndlek1j7q9t5.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'a7v3QY19iu3D_uP2TYBW14Zv'

SOCIAL_AUTH_FACEBOOK_KEY = '739607739442410'
SOCIAL_AUTH_FACEBOOK_SECRET = '8b2886bea4ee73ad698f22e57514abcd'
