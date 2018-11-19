# -*- coding: utf-8 -*-

import json
import os
import uuid
from datetime import datetime

import requests

from django.conf import settings
from django.contrib.gis.geos import Point, Polygon
from django.contrib.gis.measure import D
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Max, Min
from django.template import Context, Template

from core.utilities import extract_time
from localities.models import (
    Attribute, Changeset, Country, Domain, Locality, LocalityArchive, Specification,
    SynonymLocalities, UnconfirmedSynonym, User, Value, ValueArchive
)
from localities.tasks import regenerate_cache, regenerate_cache_cluster
from social_users.utils import get_profile


def get_what_3_words(geom):
    from requests import Timeout, ConnectionError
    try:
        what3words_api_key = settings.WHAT3WORDS_API_KEY
        api_url = settings.WHAT3WORDS_API_POS_TO_WORDS % (what3words_api_key, geom.y, geom.x)
        request = requests.get(api_url, stream=True)
        response = ''.join([line for line in request.iter_lines()])
        response = response.replace(' ', '').replace('\n', '')
        response = response.replace('}{', '},{')
        data = json.loads(response)
        if 'words' in data:
            what3words = '.'.join(data['words'])
            return what3words
        return ''
    except (Timeout, ConnectionError):
        return ''


def extract_updates(updates):
    # updates
    last_updates = []
    histories = updates
    for update in histories:
        update['locality_uuid'] = ''
        update['locality'] = ''
        if update['edit_count'] == 1:
            # get the locality to show in web
            try:
                locality = Locality.objects.get(pk=update['locality_id'])
                update['locality_uuid'] = locality.uuid
                update['locality'] = locality.name
            except Locality.DoesNotExist:
                update['locality_uuid'] = 'unknown'
                update['locality'] = 'unknown'

        if 'version' in update:
            if update['version'] == 1:
                update['mode'] = 1
            else:
                update['mode'] = 2
        else:
            update['mode'] = 1

        last_updates.append({'author': update['changeset__social_user__username'],
                             'author_nickname': update['nickname'],
                             'date_applied': update['changeset__created'],
                             'mode': update['mode'],
                             'locality': update['locality'],
                             'locality_uuid': update['locality_uuid'],
                             'data_count': update['edit_count']})
    return last_updates


def get_country_statistic(query):
    output = ''
    try:
        if query != '':
            # getting country's polygon
            country = Country.objects.get(
                name__iexact=query)
            polygons = country.polygon_geometry

            # get cache
            filename = os.path.join(
                settings.CLUSTER_CACHE_DIR,
                country.name + '_statistic'
            )
            try:
                file = open(filename, 'r')
                data = file.read()
                output = json.loads(data)
            except IOError:
                try:
                    # query for each of ATTRIBUTE
                    healthsites = get_heathsites_master().in_polygon(
                        polygons)
                    output = get_statistic(healthsites)
                    output = json.dumps(output, cls=DjangoJSONEncoder)
                    file = open(filename, 'w')
                    file.write(output)  # python will convert \n to os.linesep
                    file.close()  # you can omit in most cases as the destructor will call it
                    output = json.loads(output)
                except Exception:
                    pass
        else:
            # get cache
            filename = os.path.join(
                settings.CLUSTER_CACHE_DIR,
                'world_statistic'
            )
            try:
                file = open(filename, 'r')
                data = file.read()
                output = json.loads(data)
            except IOError:
                try:
                    if not os.path.exists(settings.CLUSTER_CACHE_DIR):
                        os.makedirs(settings.CLUSTER_CACHE_DIR)

                    # query for each of attribute
                    healthsites = get_heathsites_master()
                    output = get_statistic(healthsites)
                    output = json.dumps(output, cls=DjangoJSONEncoder)

                    file = open(filename, 'w')
                    file.write(output)  # python will convert \n to os.linesep
                    file.close()  # you can omit in most cases as the destructor will call it
                    output = json.loads(output)
                except Exception:
                    pass

    except Country.DoesNotExist:
        output = ''
    return output


def get_heathsites_master():
    return Locality.objects.filter(is_master=True).order_by('name')


def get_json_from_request(request):
    # special request:
    special_request = ['name', 'source', 'long', 'lat', 'csrfmiddlewaretoken', 'uuid']

    mstring = []
    json = {}
    for key in request.POST.iterkeys():  # 'for key in request.GET' works too.
        # Add filtering logic here.
        valuelist = request.POST.getlist(key)
        mstring.extend(['%s=%s' % (key, val) for val in valuelist])

    for str in mstring:
        req = str.split('=', 1)
        json[req[0].lower()] = req[1]
        try:
            Attribute.objects.get(key=req[0].lower())
        except Attribute.DoesNotExist:
            if req[0] not in special_request:
                tmp_changeset = Changeset.objects.create(
                    social_user=request.user
                )
                attribute = Attribute()
                attribute.key = req[0]
                attribute.changeset = tmp_changeset
                attribute.save()
                domain = Domain.objects.get(name='Health')
                specification = Specification()
                specification.domain = domain
                specification.attribute = attribute
                specification.changeset = tmp_changeset
                specification.save()

    # check mandatory
    is_valid = True
    if not json['name'] or json['name'] == '':
        is_valid = False
        json['invalid_key'] = 'name'

    if not json['lat'] or json['lat'] == '':
        is_valid = False
        json['invalid_key'] = 'latitude'

    if not json['long'] or json['long'] == '':
        is_valid = False
        json['invalid_key'] = 'longitude'

    if is_valid:
        domain = Domain.objects.get(name='Health')
        attributes = Specification.objects.filter(domain=domain).filter(required=True)
        for attribute in attributes:
            try:
                if len(json[attribute.attribute.key]) == 0:
                    is_valid = False
                    json['invalid_key'] = attribute.attribute.key
                    break
            except Exception:
                pass

    json['is_valid'] = is_valid
    return json


def get_locality_detail(locality, changes):
    # count completeness based attributes
    obj_repr = locality.repr_dict()
    # get master
    masters = []
    for val in SynonymLocalities.objects.filter(synonym_id=locality.id):
        master_uuid = val.locality.uuid
        master_name = val.locality.name
        masters.append({'name': master_name, 'uuid': master_uuid})

    # get synonyms
    synonyms = []
    for val in SynonymLocalities.objects.filter(locality_id=locality.id):
        synonym_uuid = val.synonym.uuid
        synonym_name = val.synonym.name
        synonyms.append({'name': synonym_name, 'uuid': synonym_uuid})

    # get potential master
    potential_masters = []
    for val in UnconfirmedSynonym.objects.filter(synonym_id=locality.id):
        master_uuid = val.locality.uuid
        master_name = val.locality.name
        potential_masters.append({'name': master_name, 'uuid': master_uuid})

    # get unconfirmed synonyms
    unconfirmed_synonyms = []
    for val in UnconfirmedSynonym.objects.filter(locality_id=locality.id):
        synonym_uuid = val.synonym.uuid
        synonym_name = val.synonym.name
        unconfirmed_synonyms.append({'name': synonym_name, 'uuid': synonym_uuid})

    obj_repr[u'masters'] = masters
    obj_repr[u'synonyms'] = synonyms
    obj_repr[u'potential_masters'] = potential_masters
    obj_repr[u'unconfirmed_synonyms'] = unconfirmed_synonyms
    # get latest update
    try:
        updates = []
        last_updates = locality_updates(locality.id, datetime.now())
        for last_update in last_updates:
            updates.append({'last_update': last_update['changeset__created'],
                            'uploader': last_update['changeset__social_user__username'],
                            'nickname': last_update['nickname'],
                            'changeset_id': last_update['changeset']})
        obj_repr.update({'updates': updates})
    except Exception:
        pass

    # FOR HISTORY
    obj_repr['history'] = False
    if changes:
        # get updates
        changeset = Changeset.objects.get(id=changes)
        obj_repr['updates'][0]['last_update'] = changeset.created
        obj_repr['updates'][0]['uploader'] = changeset.social_user.username
        obj_repr['updates'][0]['changeset_id'] = changes
        # get profile name
        profile = get_profile(User.objects.get(username=changeset.social_user.username))
        obj_repr['updates'][0]['nickname'] = profile.screen_name

        # check archive
        try:
            localityArchives = (
                LocalityArchive.objects.filter(changeset=changes).filter(uuid=obj_repr['uuid'])
            )
            for archive in localityArchives:
                obj_repr['geom'] = (archive.geom.x, archive.geom.y)
                obj_repr['history'] = True
        except LocalityArchive.DoesNotExist:
            pass

        try:
            localityArchives = (
                ValueArchive.objects.filter(changeset=changes).filter(locality_id=locality.id)
            )
            for archive in localityArchives:
                try:
                    specification = Specification.objects.get(id=archive.specification_id)
                    obj_repr['values'][specification.attribute.key] = archive.data
                    obj_repr['history'] = True
                except Specification.DoesNotExist:
                    pass
        except LocalityArchive.DoesNotExist:
            pass
    return obj_repr


def locality_create(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            json_request = get_json_from_request(request)
            # checking mandatory
            if json_request['is_valid'] is True:
                tmp_changeset = Changeset.objects.create(
                    social_user=request.user
                )
                # generate new uuid
                tmp_uuid = uuid.uuid4().hex

                loc = Locality()
                loc.changeset = tmp_changeset
                loc.domain = Domain.objects.get(name='Health')
                loc.uuid = tmp_uuid

                # generate unique upstream_id
                loc.upstream_id = u'web¶{}'.format(tmp_uuid)

                loc.geom = Point(
                    float(json_request['long']), float(json_request['lat'])
                )
                loc.name = json_request['name']

                loc.save()
                #  ------------------------------------------------------
                loc.set_values(json_request, request.user, tmp_changeset)

                loc.update_what3words(request.user, tmp_changeset)
                regenerate_cache.delay(tmp_changeset.pk, loc.pk)
                regenerate_cache_cluster.delay()

                return {'success': json_request['is_valid'], 'uuid': tmp_uuid, 'reason': ''}
            else:
                return {'success': json_request['is_valid'],
                        'reason': json_request['invalid_key'] + ' can not be empty'}
        else:
            return {'success': False, 'reason': 'Not Login Yet'}

    return {'success': False, 'reason': 'There is error occured'}


def locality_edit(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            json_request = get_json_from_request(request)
            # checking mandatory
            if json_request['is_valid'] is True:
                locality = Locality.objects.get(uuid=json_request['uuid'])
                old_geom = [locality.geom.x, locality.geom.y]

                locality.set_geom(float(json_request['long']), float(json_request['lat']))
                locality.name = json_request['name']

                # there are some changes so create a new changeset
                tmp_changeset = Changeset.objects.create(
                    social_user=request.user
                )
                locality.changeset = tmp_changeset

                locality.save()
                locality.set_values(json_request, request.user, tmp_changeset)

                # if location is changed
                new_geom = [locality.geom.x, locality.geom.y]
                if new_geom != old_geom:
                    locality.update_what3words(request.user, tmp_changeset)
                    regenerate_cache_cluster.delay()
                regenerate_cache.delay(tmp_changeset.id, locality.pk)

                return {
                    'success': json_request['is_valid'], 'uuid': json_request['uuid'],
                    'reason': ''
                }
            else:
                return {'success': json_request['is_valid'],
                        'reason': json_request['invalid_key'] + ' can not be empty'}
        else:
            return {'success': False, 'reason': 'Not Login Yet'}
    return {'success': False, 'reason': 'There is error occured'}


def get_statistic(healthsites):
    # locality which in polygon
    # data for frontend
    healthsites_number = healthsites.count()
    values = Value.objects.filter(locality__in=healthsites)

    hospital_number = values.filter(
        specification__attribute__key='type').filter(
        data__icontains='hospital').count()
    medical_clinic_number = values.filter(
        specification__attribute__key='type').filter(
        data__icontains='clinic').count()
    orthopaedic_clinic_number = values.filter(
        specification__attribute__key='type').filter(
        data__icontains='orthopaedic').count()

    # count completeness based attributes
    # this make long waiting, need to more good query
    complete = healthsites.filter(completeness=100).count()
    partial = healthsites.filter(completeness__gt=30).filter(completeness__lt=100).count()
    basic = healthsites.filter(completeness__lte=30).count()

    output = {
        'numbers': {
            'hospital': hospital_number,
            'medical_clinic': medical_clinic_number,
            'orthopaedic_clinic': orthopaedic_clinic_number
        },
        'completeness': {'complete': complete, 'partial': partial, 'basic': basic},
        'localities': healthsites_number
    }
    # updates
    histories = localities_updates(healthsites)
    output['last_update'] = extract_updates(histories)
    return output


def get_update_detail(update):
    profile = get_profile(User.objects.get(username=update['changeset__social_user__username']))
    update['nickname'] = profile.screen_name
    update['changeset__created'] = update['changeset__created']
    return update


def localities_updates(locality_ids):
    updates = []
    # from locality archive
    ids = LocalityArchive.objects.filter(object_id__in=locality_ids).order_by(
        '-changeset__created').values(
        'changeset', 'object_id').annotate(
        id=Min('id')).values('id')
    updates_temp = (
        LocalityArchive.objects
        .filter(object_id__in=locality_ids)
        .filter(id__in=ids)
        .order_by('-changeset__created')
        .values('changeset', 'changeset__created', 'changeset__social_user__username', 'version')
        .annotate(edit_count=Count('changeset'), locality_id=Max('object_id'))
    )
    changesets = []
    for update in updates_temp:
        changesets.append(update['changeset'])
        updates.append(get_update_detail(update))

    # get from locality if not in Locality Archive yet
    updates_temp = (
        locality_ids
        .exclude(changeset__in=changesets)
        .order_by('-changeset__created')
        .values('changeset', 'changeset__created', 'changeset__social_user__username', 'version')
        .annotate(edit_count=Count('changeset'), locality_id=Max('id'))[:15]
    )
    for update in updates_temp:
        updates.append(get_update_detail(update))

    updates.sort(key=extract_time, reverse=True)
    return updates[:10]


def locality_updates(locality_id, date):
    updates = []
    updatestemp = LocalityArchive.objects.filter(object_id=locality_id).filter(
        changeset__created__lt=date).order_by(
        '-changeset__created').values(
        'changeset', 'changeset__created', 'changeset__social_user__username').annotate(
        edit_count=Count('changeset'))[:10]
    changesets = []
    for update in updatestemp:
        changesets.append(update['changeset'])
        updates.append(get_update_detail(update))

    # get from locality if not in Locality Archive yet
    updatestemp = Locality.objects.filter(id=locality_id).values(
        'changeset', 'changeset__created', 'changeset__social_user__username').annotate(
        edit_count=Count('changeset'))
    for update in updatestemp:
        if not update['changeset'] in changesets:
            changesets.append(update['changeset'])
            updates.append(get_update_detail(update))

    updates.sort(key=extract_time, reverse=True)
    return updates[:10]


def get_locality_by_spec_data(spec, data, uuid):
    try:
        locality = Locality.objects.get(uuid=uuid)
        localities = get_heathsites_master().filter(
            geom__distance_lte=(locality.geom, D(mi=100))
        ).exclude(uuid=uuid).distance(locality.geom).order_by('-distance')
    except Locality.DoesNotExist:
        localities = get_heathsites_master()

    try:
        if spec == 'attribute':
            if uuid:
                localities = Value.objects.filter(
                    data__icontains=data).filter(locality__in=localities).values('locality')[:5]
            else:
                localities = Value.objects.filter(
                    data__icontains=data).values('locality')
        else:
            if uuid:
                localities = Value.objects.filter(
                    specification__attribute__key=spec).filter(
                    data__icontains=data).filter(locality__in=localities).values('locality')[:5]
            else:
                localities = Value.objects.filter(
                    specification__attribute__key=spec).filter(
                    data__icontains=data).values('locality')
    except Value.DoesNotExist:
        pass

    return Locality.objects.filter(id__in=localities)


def search_locality_by_spec_data(spec, data, uuid):
    localities = get_locality_by_spec_data(spec, data, uuid)
    output = get_statistic(localities)
    output['locality_name'] = ''
    output['location'] = 0.0
    if uuid:
        try:
            locality = Locality.objects.get(uuid=uuid)
            locality_name = locality.name
            output['locality_name'] = locality_name
            output['location'] = {'x': '%f' % locality.geom.x, 'y': '%f' % locality.geom.y}
        except Locality.DoesNotExist:
            pass
    output = json.dumps(output, cls=DjangoJSONEncoder)
    output = json.loads(output)
    return output


def search_locality_by_tag(query):
    try:
        localities = (
            Value.objects
            .filter(specification__attribute__key='tags')
            .filter(data__icontains='|' + query + '|').values('locality')
        )
        localities = get_heathsites_master().filter(id__in=localities)
        output = json.dumps(get_statistic(localities), cls=DjangoJSONEncoder)
        output = json.loads(output)
        return output
    except Value.DoesNotExist:
        return []


def render_fragment(template, context):
    """
    Render a template fragment using provided context
    """

    t = Template(template)
    c = Context(context)
    return t.render(c)


def parse_bbox(bbox):
    """
    Convert a textual bbox to a GEOS polygon object

    This function assumes that any raised exceptions will be handled upstream
    """

    tmp_bbox = map(float, bbox.split(','))

    if tmp_bbox[0] > tmp_bbox[2] or tmp_bbox[1] > tmp_bbox[3]:
        # bbox is not properly formatted minLng, minLat, maxLng, maxLat
        raise ValueError
    # create polygon from bbox
    return Polygon.from_bbox(tmp_bbox)
