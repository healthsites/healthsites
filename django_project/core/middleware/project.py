__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/05/19'

from django.conf import settings
from frontend.models import CampaignPage


def version(request):
    return {
        'version': settings.VERSION
    }


def FlatPageLinkMiddleware(request):
    """
    Custom middleware for flatpage links.
    """

    enrollments = CampaignPage.objects.all()
    return {
        'enrollments': enrollments
    }
