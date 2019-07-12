__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/05/19'
from frontend.models import CustomFlatPage


def version(request):
    version = None
    try:
        version_file = open('core/settings/version.txt', 'r')
        version = version_file.read().strip()
    except IOError:
        pass
    return {
        'version': version
    }


def FlatPageLinkMiddleware(request):
    """
    Custom middleware for flatpage links.
    """

    enrollments = CustomFlatPage.objects.all()
    return {
        'enrollments': enrollments
    }
