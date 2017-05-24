# -*- coding: utf-8 -*-

from django.contrib.messages import constants as messages

from .base import *  # NOQA

INSTALLED_APPS += (
    'raven.contrib.django.raven_compat',  # enable Raven plugin
    'social.apps.django_app.default',
    'pg_fts',
    'django_forms_bootstrap',
    'celery',
    'django_hashedfilenamestorage',
    'envelope',
    'pipeline',
)

# Added for python-social-auth
AUTHENTICATION_BACKENDS = (
    'social.backends.open_id.OpenIdAuth',
    'social.backends.yahoo.YahooOpenId',
    'social.backends.openstreetmap.OpenStreetMapOAuth',
    'social.backends.twitter.TwitterOAuth',
    'social.backends.github.GithubOAuth2',
    'social.backends.google.GoogleOAuth2',
    'social.backends.facebook.FacebookOAuth2',
    'social.backends.linkedin.LinkedinOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = [
    'r_basicprofile', 'r_emailaddress', 'rw_company_admin', 'w_share']

SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/'
SOCIAL_AUTH_LOGIN_URL = '/'

SOCIAL_AUTH_PIPELINE = (
    'social.pipeline.social_auth.social_details',
    'social.pipeline.social_auth.social_uid',
    'social.pipeline.social_auth.auth_allowed',
    'social.pipeline.social_auth.social_user',
    'social.pipeline.user.get_username',
    'social.pipeline.user.create_user',
    'social_users.views.save_profile',
    'social.pipeline.social_auth.associate_user',
    'social.pipeline.social_auth.load_extra_data',
    'social.pipeline.user.user_details'
)

TEMPLATE_CONTEXT_PROCESSORS += (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect')

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



DEFAULT_FILE_STORAGE = (
    'django_hashedfilenamestorage.storage.HashedFilenameFileSystemStorage'
)

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

# Project specific javascript files to be pipelined
# For third party libs like jquery should go in contrib.py
# Maybe we can split these between project-home and project-map
PIPELINE_JS['home'] = {
    'source_filenames': (
        'js/index-page.js',
    ),
    'output_filename': 'js/home.js',
}
PIPELINE_JS['map.js'] = {
    'source_filenames': (
        'js/map-page.js',
    ),
    'output_filename': 'js/map.js.js',
}

PIPELINE_JS['project'] = {
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
PIPELINE_JS['map'] = {
    'source_filenames': (
        'js/cluster-layer.js',
        'js/locality-sidebar.js',
        'js/map-functionality.js',
        'js/_app.js',
    ),
    'output_filename': 'js/map.js',
}

PIPELINE_CSS = {}

# Contributed / third party css for pipeline compression
# For hand rolled css for this app, use project.py
PIPELINE_CSS['project'] = {
    'source_filenames': (
        'css/site.css',
        'css/profile.css',
        'css/jquery.cookiebar.css'
    ),
    'output_filename': 'css/project.css',
    'extra_context': {
        'media': 'screen, projection',
    },
}

PIPELINE_CSS['map'] = {
    'source_filenames': (
        'css/map.css',
    ),
    'output_filename': 'css/map.css',
    'extra_context': {
        'media': 'screen, projection',
    },
}
PIPELINE_CSS['home'] = {
    'source_filenames': (
        'css/home.css',
    ),
    'output_filename': 'css/home.css',
    'extra_context': {
        'media': 'screen, projection',
    },
}

# These get enabled in prod.py
PIPELINE_ENABLED = False
PIPELINE_CSS_COMPRESSOR = None
PIPELINE_JS_COMPRESSOR = None


# Django envelop for contact forms
DEFAULT_FROM_EMAIL = 'enquiry@healthsites.io'
ENVELOPE_EMAIL_RECIPIENTS = ['info@healthsites.io']
ENVELOPE_SUBJECT_INTRO = '[HEALTHSITES.IO CONTACT REQUEST] '


# Override Django default message tags as recommended by envelope
MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger'  # 'error' by default
}


# WHAT3WORDS API
WHAT3WORDS_API_POS_TO_WORDS = 'https://api.what3words.com/position?key=%s&lang=en&position=%s,%s'
