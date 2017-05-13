
"""Configuration for production server"""
import os

from .prod import *  # noqa

print os.environ

DEBUG = TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

ADMINS = (
    ('Tim Sutton', 'tim@kartoza.com'),
    ('Ismail Sunni', 'ismail@kartoza.com'),
    ('Rizky Maulana Nugraha', 'rizky@kartoza.com'),)

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': os.environ['DATABASE_NAME'],
        'USER': os.environ['DATABASE_USERNAME'],
        'PASSWORD': os.environ['DATABASE_PASSWORD'],
        'HOST': os.environ['DATABASE_HOST'],
        'PORT': 5432,
        'TEST_NAME': 'unittests',
    }
}


# See fig.yml file for postfix container definition
#
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
