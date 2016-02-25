__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '25/02/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

import time
from localities.models import Locality, Value


def extract_time(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return int(time.mktime(json['changeset__created'].timetuple()))
    except KeyError:
        return 0


def extract_updates(updates):
    # updates
    last_updates = []
    histories = updates
    for update in histories:
        update['locality_uuid'] = ""
        update['locality'] = ""
        if update['edit_count'] == 1:
            # get the locality to show in web
            try:
                locality = Locality.objects.get(pk=update['locality_id'])
                locality_name = Value.objects.filter(locality=locality).filter(
                        specification__attribute__key='name')
                update['locality_uuid'] = locality.uuid
                update['locality'] = locality_name[0].data
            except Locality.DoesNotExist:
                update['locality_uuid'] = "unknown"
                update['locality'] = "unknown"

        if 'version' in update:
            if update['version'] == 1:
                update['mode'] = 1
            else:
                update['mode'] = 2
        else:
            update['mode'] = 1

        last_updates.append({"author": update['changeset__social_user__username'],
                             "author_nickname": update['nickname'],
                             "date_applied": update['changeset__created'],
                             "mode": update['mode'],
                             "locality": update['locality'],
                             "locality_uuid": update['locality_uuid'],
                             "data_count": update['edit_count']})
    return last_updates
