__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '22/01/19'

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
)
from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer, GeometrySerializerMethodField, )
from localities_osm.models.locality import (
    LocalityOSMView, LocalityOSM
)
from localities.utils import get_locality_detail

attributes_fields = LocalityOSM._meta.get_all_field_names()
attributes_fields.remove('osm_id')


class LocalityHealthsitesOSMBaseSerializer(object):
    def get_attributes(self, obj):
        attributes = {}
        for attribute in attributes_fields:
            attributes[attribute] = getattr(obj, attribute)
        return attributes

    def get_healthsites_data(self, healthsite_osm):
        # TODO: fix this

        # if healthsite_osm.osm_id and healthsite_osm.osm_type:
        #     locality_healthsites_osm = LocalityHealthsitesOSM.objects.filter(
        #         osm_id=healthsite_osm.osm_id,
        #         osm_type=healthsite_osm.osm_type
        #     )
        #     if locality_healthsites_osm.count() == 0:
        #         return {
        #             'attributes': {}
        #         }
        # else:
        #     locality_healthsites_osm = LocalityHealthsitesOSM.objects.filter(
        #         osm_pk=healthsite_osm.row.split('-')[0]
        #     )
        #     if locality_healthsites_osm.count() == 0:
        #         return {
        #             'attributes': {}
        #         }

        # get values data
        data = {}
        # locality_data = get_locality_detail(locality_healthsites_osm[0].healthsite, None)
        # data['name'] = locality_data['name']
        # data['completeness'] = locality_data['completeness']
        # data['uuid'] = locality_data['uuid']
        # data['date_modified'] = locality_data['date_modified']
        # data['attributes'] = locality_data['values']
        try:
            data['attributes']['activities'] = filter(
                None, data['attributes']['activities'].split('|'))
        except KeyError:
            pass
        try:
            data['attributes']['ancillary_services'] = filter(
                None, data['attributes']['ancillary_services'].split('|'))
        except KeyError:
            pass
        try:
            data['attributes']['notes'] = filter(
                None, data['attributes']['notes'].split('|'))
        except KeyError:
            pass
        try:
            data['attributes']['scope_of_service'] = filter(
                None, data['attributes']['scope_of_service'].split('|'))
        except KeyError:
            pass
        try:
            staff = filter(
                None, data['attributes']['staff'].split('|'))
            data['attributes']['staff'] = {
                'doctors': staff[0],
                'nurses': staff[1]
            }
        except KeyError:
            pass
        try:
            inpatient_service = filter(
                None, data['attributes']['inpatient_service'].split('|'))
            data['attributes']['inpatient_service'] = {
                'full_time_beds': inpatient_service[0],
                'part_time_beds': inpatient_service[1]
            }
        except KeyError:
            pass
        try:
            defining_hours = data['attributes'][
                'defining_hours'].split('|')
            data['attributes']['defining_hours'] = {
                'monday': filter(
                    None, defining_hours[0].split('-')),
                'tuesday': filter(
                    None, defining_hours[1].split('-')),
                'wednesday': filter(
                    None, defining_hours[2].split('-')),
                'thursday': filter(
                    None, defining_hours[3].split('-')),
                'friday': filter(
                    None, defining_hours[4].split('-')),
                'saturday': filter(
                    None, defining_hours[5].split('-')),
                'sunday': filter(
                    None, defining_hours[6].split('-'))
            }
        except (KeyError, IndexError):
            data['attributes']['defining_hours'] = {}
        try:
            data['attributes']['tags'] = filter(
                None, data['attributes']['tags'].split('|'))
        except KeyError:
            pass
        try:
            del data['attributes']['attributes']
        except KeyError:
            pass
        return data


class LocalityHealthsitesOSMSerializer(LocalityHealthsitesOSMBaseSerializer,
                                       ModelSerializer):
    geometry = GeometrySerializerMethodField
    attributes = SerializerMethodField()

    class Meta:
        model = LocalityOSMView
        exclude = []

    def get_geometry(self, obj):
        return obj.geometry.centroid

    def to_representation(self, instance):
        result = super(LocalityHealthsitesOSMSerializer, self).to_representation(instance)
        locality_data = self.get_healthsites_data(instance)
        # get healthsites locality data and put it on result attributes
        attributes = result['attributes']
        result.update(locality_data)
        for key, value in attributes.items():
            if value:
                if key == 'doctors' or key == 'nurses':
                    try:
                        locality_data['attributes']['staff'][key] = attributes[key]
                    except KeyError:
                        locality_data['attributes']['staff'] = {
                            'doctors': attributes['doctors'],
                            'nurses': attributes['nurses']
                        }
                elif key == 'full_time_beds':
                    try:
                        locality_data['attributes']['inpatient_service']['full_time_beds'] = \
                            attributes['full_time_beds']
                    except KeyError:
                        locality_data['attributes']['inpatient_service'] = {
                            'full_time_beds': attributes['full_time_beds']
                        }
                elif key == 'scope_of_service':
                    try:
                        locality_data['attributes']['scope_of_service']
                    except KeyError:
                        locality_data['attributes']['scope_of_service'] = filter(
                            None, attributes['scope_of_service'].split('|'))
                elif key == 'defining_hours':
                    continue
                else:
                    locality_data['attributes'][key] = value
        locality_data['latitude'] = self.get_geometry(instance).y
        locality_data['longitude'] = self.get_geometry(instance).x
        locality_data['row'] = result['row']
        locality_data['osm_id'] = result['osm_id']
        locality_data['osm_type'] = result['osm_type']
        return locality_data


class LocalityHealthsitesOSMGeoSerializer(LocalityHealthsitesOSMBaseSerializer,
                                          GeoFeatureModelSerializer):
    attributes = SerializerMethodField()

    class Meta:
        model = LocalityOSMView
        geo_field = 'geometry'
        exclude = attributes_fields
