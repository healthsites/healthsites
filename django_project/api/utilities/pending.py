__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '01/07/19'

from localities_osm_extension.models.pending_state import LocalityOSMExtension, \
    PendingUpdate, PendingReview
from localities_osm.models.locality import LocalityOSMView


def create_pending_update(osm_type, osm_id, osm_name, uploader, version):
    """ This will create pending of created/updated locality
    :param osm_type: the osm type of changes
    :type osm_type: str

    :param osm_id: osm id of changes
    :type osm_id: int

    :param osm_name: osm name of changes
    :type osm_name: str

    :param uploader: uploader of changes
    :type uploader: user

    :param version: version of changes
    :type version: int
    """
    try:
        PendingUpdate.objects.get(extension__osm_type=osm_type, extension__osm_id=osm_id)
        raise Exception('This osm already in pending.')
    except PendingUpdate.DoesNotExist:
        osm_extension, created = \
            LocalityOSMExtension.objects.get_or_create(
                osm_type=osm_type, osm_id=osm_id)
        pending = PendingUpdate()
        pending.extension = osm_extension
        pending.name = osm_name
        pending.uploader = uploader
        pending.version = version
        pending.save()


def create_pending_review(
        uploader, payload, reason, status_pending=None):
    """ This will create pending review of duplicated locality

    :param uploader: uploader of changes
    :type uploader: user

    :param payload: payload of changes
    :type payload: dict

    :param reason: reason of changes to be pending
    :type reason: str

    :param status_pending: status of changes to be pending
    :type status_pending: str
    """
    pending = PendingReview()
    pending.uploader = uploader
    pending.reason = reason
    pending.payload = payload

    osm_name = payload.get('tag', {}).get('name', 'no name')
    pending.name = osm_name
    if status_pending:
        pending.status = status_pending

    pending.save()


def update_pending_review(
        review_id, payload, reason, status_pending=None):
    """ This will update pending review of duplicated locality

    :param review_id: review id
    :type review_id: int

    :param payload: payload of changes
    :type payload: dict

    :param reason: reason of changes to be pending
    :type reason: str

    :param status_pending: status of changes to be pending
    :type status_pending: str
    """
    try:
        pending = PendingReview.objects.get(id=review_id)
    except PendingReview.DoesNotExist:
        raise Exception('You pushed data from unrecognized review %s' % review_id)
    pending.reason = reason
    pending.payload = payload

    osm_name = payload.get('tag', {}).get('name', 'no name')
    pending.name = osm_name
    if status_pending:
        pending.status = status_pending
    pending.save()


def delete_pending_review(review_id):
    """ This will delete pending review of duplicated locality

    :param review_id: review id
    :type review_id: int
    """
    try:
        PendingReview.objects.get(id=review_id).delete()
    except PendingReview.DoesNotExist:
        pass


def get_pending_review(review_id):
    """ This will delete pending review of duplicated locality

    :param review_id: review id
    :type review_id: int
    """
    try:
        return PendingReview.objects.get(id=review_id)
    except PendingReview.DoesNotExist:
        return None


def validate_pending_update(osm_type, osm_id):
    """ Validate pending. Delete it if it is already updated on cache.

    :param osm_id: osm id of changes
    :type osm_id: int

    :param osm_type: osm type of changes
    :type osm_type: str

    :return: Return false if not pending anymore.
    :rtype: bool
    """
    try:
        pending = PendingUpdate.objects.get(
            extension__osm_type=osm_type, extension__osm_id=osm_id)
        try:
            osm = LocalityOSMView.objects.get(
                osm_type=osm_type,
                osm_id=osm_id
            )
            if pending.version <= osm.changeset_version:
                pending.delete()
                return False
        except LocalityOSMView.DoesNotExist:
            pass
        return True
    except PendingUpdate.DoesNotExist:
        pass
    return False
