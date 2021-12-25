# coding=utf-8
"""
core.settings.contrib
"""
import os
from .base import *  # noqa
from .keys import *  # noqa

# Extra installed apps
INSTALLED_APPS = INSTALLED_APPS + (
    'rest_framework',
    'rest_framework_gis',
    'social_django',
    'celery',
    'ckeditor',
    'pipeline',
    'envelope'
)

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_URL = '/'
SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_users.middleware.save_profile',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details'
)

# PIPELINES
# Project specific javascript files to be pipelined
# For third party libs like jquery should go in contrib.py
# Maybe we can split these between project-home and project-map

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'
PIPELINE_TEMPLATE_FUNC = '_.template'  # use underscore template function
PIPELINE = {
    'PIPELINE_ENABLED': True,
    'JAVASCRIPT': {
        'outsource': {
            'source_filenames': (
                'js/mousewheel.js',
                'js/easing.js',
                'js/jquery.countto.js',
            ),
            'output_filename': 'js/outsource.js',
        },
        'home': {
            'source_filenames': (
                'libs/require.js/2.3.6/require.min.js',
                'scripts/configs/index.js'
            ),
            'output_filename': 'js/home.js',
        },
        'map': {
            'source_filenames': (
                'js/locality-sidebar.js',
            ),
            'output_filename': 'js/map.js',
        },
        'map.js': {
            'source_filenames': (
                'libs/require.js/2.3.6/require.min.js',
                'scripts/configs/map.js'
            ),
            'output_filename': 'js/map.js',
        },
        'project': {
            'source_filenames': (
                'js/utilities.js',
                'js/custom-functions.js',
                'js/cookie-bar.js',
                'js/custom-jquery.js',
                'js/csrf-ajax.js',
                'js/nav-bar.js',
                'js/google-analytics.js',
            ),
            'output_filename': 'js/project.js',
        }
    },
    'STYLESHEETS': {
        'project': {
            'source_filenames': (
                'css/site.css',
                'css/profile.css',
                'css/map/locality-sidebar.css',
                'css/map/widget/opening-hours.css',
                'css/map/modal-duplication.css',
                'css/jquery.cookiebar.css'
            ),
            'output_filename': 'css/project.css',
            'extra_context': {
                'media': 'screen, projection',
            },
        },
        'map': {
            'source_filenames': (
                'css/map.css',
            ),
            'output_filename': 'css/map.css',
            'extra_context': {
                'media': 'screen, projection',
            },
        },
        'home': {
            'source_filenames': (
                'css/home.css',
            ),
            'output_filename': 'css/home.css',
            'extra_context': {
                'media': 'screen, projection',
            },
        }
    },
    'JS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
    'CSS_COMPRESSOR': 'pipeline.compressors.yuglify.YuglifyCompressor',
}

# -------------------------------------------------- #
# ----------             OSM            ------------ #
# -------------------------------------------------- #
OSM_API_URL = 'https://api.openstreetmap.org'
AUTHENTICATION_BACKENDS = (
    'social_core.backends.openstreetmap.OpenStreetMapOAuth',
    'django.contrib.auth.backends.ModelBackend',
)
