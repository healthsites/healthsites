# -*- coding: utf-8 -*-

from .project import *  # noqa

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
# Changes for live site
# ['*'] for testing but not for production

ALLOWED_HOSTS = ['*']

# Comment if you are not running behind proxy
USE_X_FORWARDED_HOST = True

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False


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
        'logfile': {
            'class': 'logging.FileHandler',
            'filename': '/tmp/tmd-web.log',
            'formatter': 'verbose',
            'level': 'INFO',
        }
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['logfile'],
            'level': 'INFO',  # switch to DEBUG to show actual SQL
        },
        'django': {
            'handlers': ['logfile'],
            'level': 'INFO'
        }
    },
    # root logger
    # non handled logs will propagate to the root logger
    'root': {
        'handlers': ['logfile'],
        'level': 'INFO'
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Host for sending e-mail.
EMAIL_HOST = 'smtp'
# Port for sending e-mail.
EMAIL_PORT = 25
# SMTP authentication information for EMAIL_HOST.
# See fig.yml for where these are defined
EMAIL_HOST_USER = 'noreply@healthsites.io'
EMAIL_HOST_PASSWORD = 'docker'
EMAIL_USE_TLS = False
EMAIL_SUBJECT_PREFIX = '[healthsites]'

CLUSTER_CACHE_DIR = '/data/cache'
MEDIA_ROOT = '/data/media'

BROKER_URL = 'amqp://guest:guest@rabbitmq:5672//'
