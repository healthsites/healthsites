# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '18/03/16'
__license__ = "GPL"
__copyright__ = 'kartoza.com'

import json
import os
import uuid
from core.utilities import extract_time
from datetime import datetime
from django.conf import settings
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import Count, Max
from localities.models import Attribute, Changeset, Country, Domain, Locality, LocalityArchive, Specification, User, \
    Value, ValueArchive
from localities.tasks import regenerate_cache
from social_users.views import getProfile
from localities.utils import render_fragment

limit = 100


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


def get_country_statistic(query):
    output = ""
    try:
        if query != "":
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
            except IOError as e:
                try:
                    # query for each of attribute
                    healthsites = Locality.objects.in_polygon(
                            polygons)
                    output = get_statistic(healthsites)
                    result = json.dumps(output, cls=DjangoJSONEncoder)
                    file = open(filename, 'w')
                    file.write(result)  # python will convert \n to os.linesep
                    file.close()  # you can omit in most cases as the destructor will call it
                except Exception as e:
                    print e
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
            except IOError as e:
                try:
                    # query for each of attribute
                    healthsites = Locality.objects.all()
                    output = get_statistic(healthsites)
                    result = json.dumps(output, cls=DjangoJSONEncoder)
                    file = open(filename, 'w')
                    file.write(result)  # python will convert \n to os.linesep
                    file.close()  # you can omit in most cases as the destructor will call it
                except Exception as e:
                    print e

    except Country.DoesNotExist:
        output = ""
    return output


def get_heathsite_by_polygon(request, polygon):
    healthsites = Locality.objects.in_polygon(
            polygon)

    facility_type = ""
    if 'facility_type' in request.GET:
        facility_type = request.GET['facility_type']

    output = []
    index = 1;
    for healthsite in healthsites:
        if healthsite.is_type(facility_type):
            output.append(healthsite.repr_dict())
            index += 1
        if index == limit:
            break
    return output


def get_json_from_request(request):
    # special request:
    special_request = ["long", "lat", "csrfmiddlewaretoken", "uuid"]

    mstring = []
    json = {}
    for key in request.POST.iterkeys():  # "for key in request.GET" works too.
        # Add filtering logic here.
        valuelist = request.POST.getlist(key)
        mstring.extend(['%s=%s' % (key, val) for val in valuelist])

    for str in mstring:
        req = str.split('=', 1)
        json[req[0].lower()] = req[1]
        try:
            Attribute.objects.get(key=req[0].lower())
        except:
            if req[0] not in special_request:
                tmp_changeset = Changeset.objects.create(
                        social_user=request.user
                )
                attribute = Attribute()
                attribute.key = req[0]
                attribute.changeset = tmp_changeset
                attribute.save()
                domain = Domain.objects.get(name="Health")
                specification = Specification()
                specification.domain = domain
                specification.attribute = attribute
                specification.changeset = tmp_changeset
                specification.save()

    # check mandatory
    is_valid = True

    if not json['lat'] or json['lat'] == "":
        is_valid = False
        json['invalid_key'] = "latitude"

    if not json['long'] or json['long'] == "":
        is_valid = False
        json['invalid_key'] = "longitude"

    if is_valid:
        domain = Domain.objects.get(name="Health")
        attributes = Specification.objects.filter(domain=domain).filter(required=True)
        for attribute in attributes:
            try:
                if len(json[attribute.attribute.key]) == 0:
                    is_valid = False
                    json['invalid_key'] = attribute.attribute.key
                    break
            except:
                print "except"

    json['is_valid'] = is_valid
    return json


def get_locality_detail(locality, changes):
    # get attributes
    attribute_count = 18
    # count completeness based attributes
    obj_repr = locality.repr_dict()
    data_repr = render_fragment(
            locality.domain.template_fragment, obj_repr
    )

    num_data = len(obj_repr['values']) + 1  # geom
    completeness = (num_data + 0.0) / (attribute_count + 0.0) * 100  # percentage
    obj_repr.update({'completeness': '%s%%' % format(completeness, '.2f')})

    # get latest update
    try:
        updates = []
        last_updates = locality_updates(locality.id, datetime.now())
        for last_update in last_updates:
            updates.append({"last_update": last_update['changeset__created'],
                            "uploader": last_update['changeset__social_user__username'],
                            "nickname": last_update['nickname'],
                            "changeset_id": last_update['changeset']});
        obj_repr.update({'updates': updates})
    except Exception as e:
        print e

    # FOR HISTORY
    obj_repr['history'] = False
    print obj_repr['updates'][0]
    if changes:
        changeset = Changeset.objects.get(id=changes)
        obj_repr['updates'][0]['last_update'] = changeset.created
        obj_repr['updates'][0]['uploader'] = changeset.social_user.username

        # get profile name
        profile = getProfile(User.objects.get(username=changeset.social_user.username))
        obj_repr['updates'][0]['nickname'] = profile.screen_name
        obj_repr['updates'][0]['changeset_id'] = changes
        print obj_repr['updates'][0]
        try:
            localityArchives = LocalityArchive.objects.filter(changeset=changes).filter(uuid=obj_repr['uuid'])
            for archive in localityArchives:
                obj_repr['geom'] = (archive.geom.x, archive.geom.y)
                obj_repr['history'] = True
        except LocalityArchive.DoesNotExist:
            print "next"

        try:
            localityArchives = ValueArchive.objects.filter(changeset=changes).filter(locality_id=locality.id)
            for archive in localityArchives:
                try:
                    specification = Specification.objects.get(id=archive.specification_id)
                    obj_repr['values'][specification.attribute.key] = archive.data
                    obj_repr['history'] = True
                except Specification.DoesNotExist:
                    print "next"
        except LocalityArchive.DoesNotExist:
            print "next"
    return obj_repr


def locality_create(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            json_request = get_json_from_request(request)
            # checking mandatory
            if json_request['is_valid'] == True:
                tmp_changeset = Changeset.objects.create(
                        social_user=request.user
                )
                # generate new uuid
                tmp_uuid = uuid.uuid4().hex

                loc = Locality()
                loc.changeset = tmp_changeset
                loc.domain = Domain.objects.get(name="Health")
                loc.uuid = tmp_uuid

                # generate unique upstream_id
                loc.upstream_id = u'web¶{}'.format(tmp_uuid)

                loc.geom = Point(
                        float(json_request['long']), float(json_request['lat'])
                )
                loc.save()
                loc.set_values(json_request, request.user, tmp_changeset)

                regenerate_cache.delay(tmp_changeset.pk, loc.pk)

                return {"success": json_request['is_valid'], "uuid": tmp_uuid, "reason": ""}
            else:
                return {"success": json_request['is_valid'], "reason": json_request['invalid_key'] + " can not be empty"}
        else:
            return {"success": False, "reason": "Not Login Yet"}

    return {"success": False, "reason": "There is error occured"}


def locality_edit(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            json_request = get_json_from_request(request)
            # checking mandatory
            if json_request['is_valid'] == True:
                locality = Locality.objects.get(uuid=json_request['uuid'])
                locality.set_geom(float(json_request['long']), float(json_request['lat']))
                # there are some changes so create a new changeset
                tmp_changeset = Changeset.objects.create(
                        social_user=request.user
                )
                locality.changeset = tmp_changeset
                locality.save()
                locality.set_values(json_request, request.user, tmp_changeset)

                regenerate_cache.delay(tmp_changeset.pk, locality.pk)

                return {"success": json_request['is_valid'], "uuid": json_request['uuid'], "reason": ""}
            else:
                return {"success": json_request['is_valid'], "reason": json_request['invalid_key'] + " can not be empty"}
        else:
            return {"success": False, "reason": "Not Login Yet"}
    return {"success": False, "reason": "There is error occured"}


def get_statistic(healthsites):
    # locality which in polygon
    # data for frontend
    complete = 0
    partial = 0
    basic = 0

    healthsites_number = healthsites.count()
    values = Value.objects.filter(locality__in=healthsites)

    hospital_number = values.filter(
            specification__attribute__key='type').filter(
            data__iexact='hospital').count()
    medical_clinic_number = values.filter(
            specification__attribute__key='type').filter(
            data__iexact='clinic').count()
    orthopaedic_clinic_number = values.filter(
            specification__attribute__key='type').filter(
            data__iexact='orthopaedic').count()

    # check completnees
    values = Value.objects.filter(locality__in=healthsites).exclude(data__isnull=True).exclude(
            data__exact='').values('locality').annotate(
            value_count=Count('locality'))
    # get attributes
    attribute_count = 18
    # count completeness based attributes
    # this make long waiting, need to more good query
    complete = values.filter(value_count__gte=attribute_count).count()
    partial = values.filter(value_count__gte=4).filter(value_count__lte=attribute_count - 1).count()
    basic = values.filter(value_count__lte=3).count()

    output = {"numbers": {"hospital": hospital_number, "medical_clinic": medical_clinic_number
        , "orthopaedic_clinic": orthopaedic_clinic_number},
              "completeness": {"complete": complete, "partial": partial, "basic": basic},
              "localities": healthsites_number}
    # updates
    histories = localities_updates(healthsites)
    output["last_update"] = extract_updates(histories)
    return output


def localities_updates(locality_ids):
    updates = []
    try:
        updates1 = LocalityArchive.objects.filter(object_id__in=locality_ids).order_by(
                '-changeset__created').values(
                'changeset', 'changeset__created', 'changeset__social_user__username', 'version').annotate(
                edit_count=Count('changeset'), locality_id=Max('object_id'))[:15]
        for update in updates1:
            updates.append(update)
        updates2 = ValueArchive.objects.filter(locality_id__in=locality_ids).filter(version__gt=1).order_by(
                '-changeset__created').values(
                'changeset', 'changeset__created', 'changeset__social_user__username', 'version').annotate(
                edit_count=Count('changeset'), locality_id=Max('locality_id'))[:15]
        for update in updates2:
            updates.append(update)
        updates.sort(key=extract_time, reverse=True)
    except LocalityArchive.DoesNotExist:
        print "Locality Archive not exist"

    output = []
    prev_changeset = 0
    for update in updates:
        if prev_changeset != update['changeset']:
            profile = getProfile(User.objects.get(username=update['changeset__social_user__username']))
            update['nickname'] = profile.screen_name
            update['changeset__created'] = str(update['changeset__created'])
            output.append(update)
        prev_changeset = update['changeset']
    return output[:10]


def locality_updates(locality_id, date):
    updates = []
    try:
        updates1 = LocalityArchive.objects.filter(object_id=locality_id).filter(changeset__created__lt=date).order_by(
                '-changeset__created').values(
                'changeset', 'changeset__created', 'changeset__social_user__username').annotate(
                edit_count=Count('changeset'))[:15]
        for update in updates1:
            updates.append(update)
        updates2 = ValueArchive.objects.filter(locality_id=locality_id).filter(
                changeset__created__lt=date).order_by(
                '-changeset__created').values(
                'changeset', 'changeset__created', 'changeset__social_user__username').annotate(
                edit_count=Count('changeset'))[:15]
        for update in updates2:
            updates.append(update)
        updates.sort(key=extract_time, reverse=True)
    except LocalityArchive.DoesNotExist:
        print "Locality Archive not exist"

    output = []
    prev_changeset = 0
    for update in updates:
        if prev_changeset != update['changeset']:
            profile = getProfile(User.objects.get(username=update['changeset__social_user__username']))
            update['nickname'] = profile.screen_name
            update['changeset__created'] = str(update['changeset__created'])
            output.append(update)
        prev_changeset = update['changeset']
    return output[:10]


def get_locality_by_spec_data(spec, data, uuid):
    try:
        if spec == "attribute":
            if uuid:
                locality = Locality.objects.get(uuid=uuid)
                localities = Locality.objects.filter(
                        geom__distance_lte=(locality.geom, D(mi=100))
                ).exclude(uuid=uuid).distance(locality.geom).order_by('-distance')
                localities = Value.objects.filter(
                        data__icontains=data).filter(locality__in=localities).values('locality')[:5]
            else:
                localities = Value.objects.filter(
                        data__icontains=data).values('locality')
        else:
            if uuid:
                locality = Locality.objects.get(uuid=uuid)
                localities = Locality.objects.filter(
                        geom__distance_lte=(locality.geom, D(mi=100))
                ).exclude(uuid=uuid).distance(locality.geom).order_by('-distance')
                localities = Value.objects.filter(
                        specification__attribute__key=spec).filter(
                        data__icontains=data).filter(locality__in=localities).values('locality')[:5]
            else:
                localities = Value.objects.filter(
                        specification__attribute__key=spec).filter(
                        data__icontains=data).values('locality')
        return localities
    except Value.DoesNotExist:
        return []


def search_locality_by_spec_data(spec, data, uuid):
    localities = get_locality_by_spec_data(spec, data, uuid)
    print localities
    if localities == []:
        return []
    else:
        output = get_statistic(localities)
        output['locality_name'] = ""
        output['location'] = 0.0
        if uuid:
            try:
                locality = Locality.objects.get(uuid=uuid)
                locality_name = Value.objects.filter(locality=locality).filter(
                        specification__attribute__key='name')[0].data
                output['locality_name'] = locality_name
                output['location'] = {'x': "%f" % locality.geom.x, 'y': "%f" % locality.geom.y}
            except Locality.DoesNotExist:
                print "locality not found"
        return output


def search_locality_by_tag(query):
    try:
        localities = Value.objects.filter(
                specification__attribute__key='tags').filter(data__icontains="|" + query + "|").values('locality')
        return get_statistic(localities)
    except Value.DoesNotExist:
        return []
