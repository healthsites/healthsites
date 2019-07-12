__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '01/07/19'

from localities_osm_extension.models.pending_state import LocalityOSMExtension, \
    PendingUpdate, PendingReview
from localities_osm.models.locality import LocalityOSMView


def create_pending_update(osm_type, osm_id, osm_name, uploader, version):
    """ This will create pending of created/updated locality """
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


def create_pending_review(uploader, osm_name, payload, reason):
    """ This will create pending review of duplicated locality """
    pending = PendingReview()
    pending.uploader = uploader
    pending.name = osm_name
    pending.reason = reason
    pending.payload = payload
    pending.save()


def validate_pending_update(osm_type, osm_id):
    """ Validate pending. Delete it if it is already updated on cache.
    Return false if not pending anymore.
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
