# -*- coding: utf-8 -*-

from django.utils.translation import ugettext_lazy as _

from .celery_setting import *  # noqa
from .contrib import *  # noqa

# Project apps
INSTALLED_APPS += (
    'localities',
    'frontend',
    'social_users',
    'api',
)

# How many versions to list in each project box
PROJECT_VERSION_LIST_SIZE = 10

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

# Set languages which want to be translated
LANGUAGES = (
    ('en', _('English')),
    ('af', _('Afrikaans')),
    ('id', _('Indonesian')),
    ('ko', _('Korean')),
)

# Set storage path for the translation files
LOCALE_PATHS = [ABS_PATH('locale')]

# Cache folder
CLUSTER_CACHE_DIR = ABS_PATH('cache')
CLUSTER_CACHE_MAX_ZOOM = 5


# authentication settings
ANONYMOUS_USER_ID = -1
# AUTH_USER_MODULE = 'social_users.Profile'
LOGIN_REDIRECT_URL = '/profile/%(username)s/'
LOGIN_URL = '/signin/'
LOGOUT_URL = '/logout/'
