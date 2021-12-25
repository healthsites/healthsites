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
    # 'pipeline',
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
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# TODO:
#  Fix this
#  There are javascript that is not working with pipeline
# PIPELINE_TEMPLATE_FUNC = '_.template'  # use underscore template function
# PIPELINE = {
#     'PIPELINE_ENABLED': True,
#     'JAVASCRIPT': {
#         'base_library': {
#             'source_filenames': (
#                 'libs/jquery.js/3.3.1/jquery.min.js',
#                 'libs/jquery-ui/1.12.1/jquery-ui.min.js',
#                 'libs/bootstrap/3.3.5/js/bootstrap.min.js',
#                 'libs/jquery.slick/1.5.7/slick.js',
#                 'libs/jquery.timepicker/1.10.1/jquery.timepicker.min.js'
#             ),
#             'output_filename': 'js/base_libs.js',
#         },
#         'project': {
#             'source_filenames': (
#                 'js/global/utilities.js',
#                 'js/global/custom-functions.js',
#                 'js/global/cookie-bar.js',
#                 'js/global/custom-jquery.js',
#                 'js/global/csrf-ajax.js',
#                 'js/global/nav-bar.js',
#                 'js/global/google-analytics.js',
#             ),
#             'output_filename': 'js/project.js',
#         },
#         'basic_map': {
#             'source_filenames': (
#                 'libs/js-signals/1.0.0/js-signals.min.js',
#                 'libs/d3/3.5.7/d3.min.js',
#                 'libs/c3/0.4.10/c3.min.js',
#                 'libs/hasher/1.2.0/hasher.min.js',
#                 'libs/crossroads/0.12.2/crossroads.min.js',
#                 'js/locality-sidebar.js',
#             ),
#             'output_filename': 'js/basic_map.js',
#         },
#
#         'outsource': {
#             'source_filenames': (
#                 'js/mousewheel.js',
#                 'js/easing.js',
#                 'js/jquery.countto.js',
#                 'libs/require.js/2.3.6/require.min.js',
#             ),
#             'output_filename': 'js/outsource.js',
#         },
#         'map': {
#             'source_filenames': (
#                 'js/locality-sidebar.js',
#             ),
#             'output_filename': 'js/map.js',
#         },
#     },
#     'STYLESHEETS': {
#         'base_library': {
#             'source_filenames': (
#                 'libs/font-awesome/4.4.0/css/font-awesome.min.css',
#                 'libs/jquery-ui/1.11.4/jquery-ui.min.css',
#                 'libs/jquery.slick/1.5.7/slick.css',
#                 'libs/c3/0.4.10/c3.min.css',
#                 'libs/bootstrap/3.3.5/css/bootstrap.min.css',
#                 'libs/fonts.googleapis.com/Raleway.css',
#                 'libs/fonts.googleapis.com/Ubuntu.css'
#             ),
#             'extra_context': {
#                 'media': 'screen, projection',
#             },
#             'output_filename': 'js/base_libs.css',
#         },
#         'project': {
#             'source_filenames': (
#                 'css/site.css',
#                 'css/jquery.cookiebar.css',
#                 'css/profile.css',
#             ),
#             'output_filename': 'css/project.css',
#             'extra_context': {
#                 'media': 'screen, projection',
#             },
#         },
#         'base': {
#             'source_filenames': (
#                 'css/site.css',
#                 'css/home.css',
#             ),
#             'output_filename': 'css/base.css',
#             'extra_context': {
#                 'media': 'screen, projection',
#             },
#         },
#         'map': {
#             'source_filenames': (
#                 'libs/leaflet/0.7.7/leaflet.css',
#                 'libs/leaflet.draw/0.2.3/leaflet.draw.css',
#                 'css/map/locality-sidebar.css',
#                 'css/map/widget/opening-hours.css',
#                 'css/map/modal-duplication.css',
#             ),
#             'output_filename': 'css/map.css',
#             'extra_context': {
#                 'media': 'screen, projection',
#             },
#         },
#     },
#     'JS_COMPRESSOR': 'pipeline.compressors.yui.YUICompressor',
#     'CSS_COMPRESSOR': 'pipeline.compressors.yui.YUICompressor'
# }

# -------------------------------------------------- #
# ----------             OSM            ------------ #
# -------------------------------------------------- #
OSM_API_URL = 'https://api.openstreetmap.org'
AUTHENTICATION_BACKENDS = (
    'social_core.backends.openstreetmap.OpenStreetMapOAuth',
    'django.contrib.auth.backends.ModelBackend',
)
