# -*- coding: utf-8 -*-
from .test import *

INSTALLED_APPS += (
    'django_jenkins',  # don't remove this comma
)

# -----------------------------------------------------------------------------
# For django coverage support when testing
# -----------------------------------------------------------------------------

# exclude files/folders, wildcards accepted
COVERAGE_EXCLUDES_FOLDERS = [
    '*settings/*',
    '*tests*'
]

NOSE_ARGS = [
    # 'django_app',
]

PYLINT_RCFILE = 'pylint.rc'
#
# For django-jenkins integration
#
PROJECT_APPS = (
    # django_app,
)

JENKINS_TASKS = (
    'django_jenkins.tasks.with_coverage',
    'django_jenkins.tasks.run_pylint',
    # 'django_jenkins.tasks.django_tests',
    'django_jenkins.tasks.run_pep8',
    # Needs rhino or nodejs
    # 'django_jenkins.tasks.run_jshint',
    # Needs rhino or nodejs
    # 'django_jenkins.tasks.run_csslint',
    'django_jenkins.tasks.run_pyflakes',
    'django_jenkins.tasks.run_sloccount'
)

# added nose_test_runner for jenkins
# this feature is currently in git master
# commit 2f241bb6b7a111172f1e5bd26a1d21815f83d1e7
JENKINS_TEST_RUNNER = 'django_jenkins.nose_runner.CINoseTestSuiteRunner'
