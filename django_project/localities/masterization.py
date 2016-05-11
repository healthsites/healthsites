__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '11/05/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

from .models import Locality, SynonymLocalities, UnconfirmedSynonym


def report_locality_as_unconfirmed_synonym(locality_id, master_id):
    # locality_id = locality of id that will be downgrade:
    # master_id = locality of id that is the masters
    # Report a locality as unconfirmed synonym
    try:
        # get the locality
        locality = Locality.objects.get(id=locality_id)
        master = Locality.objects.get(id=master_id)
        try:
            UnconfirmedSynonym.objects.get(locality=master, synonym=locality)
        except UnconfirmedSynonym.DoesNotExist:
            UnconfirmedSynonym(locality=master, synonym=locality).save()
        return True
    except Locality.DoesNotExist:
        return False
    except Exception as e:
        print e


def reject_unnconfirmed_synonym(id):
    # id = unconfirmed synonyms relationship id
    # reject unconfirmed synonym
    try:
        # get unconfirmed
        unconfirmed_synonym = UnconfirmedSynonym.objects.get(id=id)
        unconfirmed_synonym.delete()
        return True
    except UnconfirmedSynonym.DoesNotExist:
        return False


def promote_unconfirmed_synonym(id):
    # id = unconfirmed synonyms relationship id
    # Promote unconfirmed synonym to a synonym
    # made it's master as is master
    try:
        # get unconfirmed
        unconfirmed_synonym = UnconfirmedSynonym.objects.get(id=id)
        result = downgrade_master_as_synonyms(unconfirmed_synonym.synonym.id, unconfirmed_synonym.locality.id)
        if result:
            unconfirmed_synonym.delete()
        return result
    except UnconfirmedSynonym.DoesNotExist:
        return False


def promote_synonym_as_master(locality_id):
    # locality_id = locality of id that will be promoted
    # promote a synonym as master
    try:
        # get the locality
        locality = Locality.objects.get(id=locality_id)
        if not locality.is_master:
            locality.is_master = True
            locality.save()
        # check all of this locality as unconfirmed and confirmed synonym
        SynonymLocalities.objects.filter(synonym=locality).delete()
        # it can be synonym but not confirmed yet
        # UnconfirmedSynonym.objects.filter(synonym=locality).delete()
        return True
    except Locality.DoesNotExist:
        return False


def downgrade_master_as_synonyms(locality_id, master_id):
    # locality_id = locality of id that will be downgrade:
    # master_id = locality of id that is the masters
    # downgrade master to other synonym
    try:
        # get the locality
        # preparing
        locality = Locality.objects.get(id=locality_id)
        master = Locality.objects.get(id=master_id)
        if locality.is_master:
            locality.is_master = False
            locality.save()

        promote_synonym_as_master(master_id)
        # create synonym relationship
        try:
            SynonymLocalities.objects.get(locality=master, synonym=locality)
        except SynonymLocalities.DoesNotExist:
            SynonymLocalities(locality=master, synonym=locality).save()

        # check all of this other synonyms that this locality as master
        for synonym in SynonymLocalities.objects.filter(locality=locality):
            synonym.locality = master
            synonym.save()
        return True
    except Locality.DoesNotExist:
        return False
