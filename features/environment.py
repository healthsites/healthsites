"""Behave test environment for the Healthsites Django project."""
import os
import sys
from pathlib import Path

import django
from django.test.runner import DiscoverRunner


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DJANGO_PROJECT_PATH = PROJECT_ROOT / 'django_project'

if str(DJANGO_PROJECT_PATH) not in sys.path:
    sys.path.insert(0, str(DJANGO_PROJECT_PATH))


def before_all(context):
    """Initialise Django so behave can use the ORM and test client."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.tests')
    django.setup()
    context.test_runner = DiscoverRunner()
    context.test_runner.setup_test_environment()
    context.databases = context.test_runner.setup_databases()


def after_all(context):
    """Tear down the Django testing environment and databases."""
    context.test_runner.teardown_databases(context.databases)
    context.test_runner.teardown_test_environment()


def after_feature(context, feature):
    """Ensure URL-based features exercised every discovered path."""
    if getattr(context, 'url_tracking_initialised', False):
        missing = sorted(context.remaining_urls)
        assert not missing, (
            'Missing Behave scenarios for the following URLs: ' + ', '.join(missing)
        )
        del context.remaining_urls
        del context.testable_urls
        context.url_tracking_initialised = False


def before_scenario(context, scenario):
    """Provide a Django test client for each scenario."""
    from django.test import Client

    context.client = Client()
