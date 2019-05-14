__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/05/19'


def version(request):
    version = None
    try:
        version_file = open("core/settings/version.txt", "r")
        version = version_file.read().strip()
    except IOError:
        pass
    return {
        'version': version
    }
