
from .project import *  # noqa

# http://hustoknow.blogspot.com/2011/02/setting-up-django-nose-on-hudson.html
INSTALLED_APPS += (
    'django_nose',  # don't remove this comma
)

TEST_RUNNER = 'django.test.runner.DiscoverRunner'

NOSE_ARGS = (
    '--with-coverage',
    '--cover-erase',
    '--cover-html',
    '--cover-html-dir=xmlrunner/html',
    '--cover-inclusive',
    # '--cover-package=django_app',
    '--nocapture',
    '--nologcapture'
)


EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
# change this to a proper location
EMAIL_FILE_PATH = '/tmp/'


LOGGING = {
    # internal dictConfig version - DON'T CHANGE
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'nullhandler': {
            'class': 'logging.NullHandler',
        },
    },
    # default root logger
    'root': {
        'level': 'DEBUG',
        'handlers': ['nullhandler'],
    }
}
