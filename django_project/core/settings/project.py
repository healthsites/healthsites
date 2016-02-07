# coding=utf-8

"""Project level settings.

Adjust these values as needed but don't commit passwords etc. to any public
repository!
"""

import os  # noqa
from django.utils.translation import ugettext_lazy as _
from .utils import absolute_path
from .contrib import *  # noqa
from .secret import *  # secret

# Project apps
INSTALLED_APPS += (
    'localities',
    'frontend',
    'social_users',
    'api',
    'django_hashedfilenamestorage',
    'envelope'
)

# How many versions to list in each project box
PROJECT_VERSION_LIST_SIZE = 10

# Set debug to false for production
DEBUG = TEMPLATE_DEBUG = False

SOUTH_TESTS_MIGRATE = False

# Set languages which want to be translated
LANGUAGES = (
    ('en', _('English')),
    ('af', _('Afrikaans')),
    ('id', _('Indonesian')),
    ('ko', _('Korean')),
)

# Set storage path for the translation files
LOCALE_PATHS = (absolute_path('locale'),)

# Project specific javascript files to be pipelined
# For third party libs like jquery should go in contrib.py
# Maybe we can split these between project-home and project-map
PIPELINE_JS['project'] = {
    'source_filenames': (
        'js/utilities.js',
        'js/clusterLayer.js',
        'js/csrf-ajax.js',
        'js/nav_bar.js',
        'js/localitySidebar.js',
        'js/map.js',
        'js/app.js',
    ),
    'output_filename': 'js/project.js',
}

# Project specific css files to be pipelined
# For third party libs like bootstrap should go in contrib.py
PIPELINE_CSS['project'] = {
    'source_filenames': (
        'css/site.css',
        'css/profile.css',
    ),
    'output_filename': 'css/project.css',
    'extra_context': {
        'media': 'screen, projection',
    },
}


# define cluster cache directory (directory must exist)
CLUSTER_CACHE_DIR = '/tmp'
