# -*- coding: utf-8 -*-
import os

from .base import *  # NOQA

# Extra installed apps
INSTALLED_APPS = (
                     # 'grappelli',
                 ) + INSTALLED_APPS

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',  # enable Raven plugin
    'social_django',
    'pg_fts',
    'django_forms_bootstrap',
    'celery',
    'rest_framework',
    'rest_framework_gis',
    'django.contrib.gis'
)

STOP_WORDS = (
    'a', 'an', 'and', 'if', 'is', 'the', 'in', 'i', 'you', 'other',
    'this', 'that'
)

CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Added for userena
AUTHENTICATION_BACKENDS = (
    'social_core.backends.openstreetmap.OpenStreetMapOAuth',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = [
    'r_basicprofile', 'r_emailaddress', 'rw_company_admin', 'w_share']

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_URL = '/'

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_users.views.save_profile',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details'
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'social_django.context_processors.backends',
    'social_django.context_processors.login_redirect')

# TEMPLATES = [
#     {
#         'BACKEND': 'django.template.backends.django.DjangoTemplates',
#         'DIRS': [os.path.join(BASE_DIR, 'templates')],
#         'APP_DIRS': True,
#         'OPTIONS': {
#             'context_processors': TEMPLATE_CONTEXT_PROCESSORS,
#         },
#     },
# ]

ANONYMOUS_USER_ID = -1
AUTH_PROFILE_MODULE = 'accounts.Profile'
LOGIN_REDIRECT_URL = '/accounts/%(username)s/'
LOGIN_URL = '/accounts/signin/'
LOGOUT_URL = '/accounts/signout/'

# Easy-thumbnails options
THUMBNAIL_SUBDIR = 'thumbnails'
THUMBNAIL_ALIASES = {
    '': {
        'entry': {'size': (50, 50), 'crop': True},
        'medium-entry': {'size': (100, 100), 'crop': True},
        'large-entry': {'size': (400, 300), 'crop': True},
        'thumb300x200': {'size': (300, 200), 'crop': True},
    },
}

# Pipeline related settings

INSTALLED_APPS += (
    'pipeline',)

MIDDLEWARE_CLASSES += (
    # For rosetta localisation
    'django.middleware.locale.LocaleMiddleware',
)

DEFAULT_FILE_STORAGE = (
    'django_hashedfilenamestorage.storage.HashedFilenameFileSystemStorage')

# use underscore template function
PIPELINE_TEMPLATE_FUNC = '_.template'

# enable cached storage - requires uglify.js (node.js)
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

# Contributed / third party js libs for pipeline compression
# For hand rolled js for this app, use project.py
# Only put css and libs in here that are not available on CDN
PIPELINE_JS = {
    'outsource': {
        'source_filenames': (
            'js/mousewheel.js',
            'js/easing.js',
            'js/jquery.countto.js',
        ),
        'output_filename': 'js/outsource.js',
    },
}

PIPELINE_CSS = {}

# These get enabled in prod.py
PIPELINE_ENABLED = False
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None

BROKER_URL = 'amqp://guest:guest@%s:5672//' % os.environ['RABBITMQ_HOST']

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# Django envelop for contact forms
DEFAULT_FROM_EMAIL = 'enquiry@healthsites.io'
ENVELOPE_EMAIL_RECIPIENTS = ['info@healthsites.io']
ENVELOPE_SUBJECT_INTRO = '[HEALTHSITES.IO CONTACT REQUEST] '
