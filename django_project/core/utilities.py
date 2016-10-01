import time

__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '25/02/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'


def extract_time(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return int(time.mktime(json['changeset__created'].timetuple()))
    except KeyError:
        return 0
