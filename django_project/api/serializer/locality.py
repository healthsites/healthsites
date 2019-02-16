__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField)
from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer, GeometrySerializerMethodField)
from localities.models import Locality


class LocalitySerializerBase(object):
    def get_attributes(self, obj):
        """ Serializing attributes of locality
        """
        dict = obj.repr_dict(in_array=True)
        dict = dict['values']

        # serializing beds
        try:
            full_time_beds = '-'
            part_time_beds = '-'
            try:
                full_time_beds = dict['inpatient_service'][0]
            except KeyError:
                pass
            try:
                part_time_beds = dict['inpatient_service'][1]
            except KeyError:
                pass
            dict['inpatient_service'] = {
                'full_time_beds': full_time_beds,
                'part_time_beds': part_time_beds
            }
        except KeyError:
            pass

        # Defining Hours
        defining_hours = {}
        for index, day in enumerate(Locality.DEFINED_DAYS):
            defining_hours[day] = '-'
            try:
                hours = dict['defining_hours'][index].split('-')
                defining_hours[day] = []
                try:
                    if hours[0] and hours[1]:
                        defining_hours[day].append(hours[0] + '-' + hours[1])
                except IndexError:
                    pass
                try:
                    if hours[2] and hours[3]:
                        defining_hours[day].append(hours[2] + '-' + hours[3])
                except IndexError:
                    pass
            except KeyError:
                pass
        dict['defining_hours'] = defining_hours

        # serializing staff
        try:
            doctors = '-'
            nurses = '-'
            try:
                doctors = dict['doctors']
            except KeyError:
                pass
            try:
                nurses = dict['nurses']
            except KeyError:
                pass
            dict['staff'] = {
                'doctors': doctors,
                'nurses': nurses
            }
        except KeyError:
            pass
        return dict


class LocalitySerializer(LocalitySerializerBase, ModelSerializer):
    location = GeometrySerializerMethodField
    date_modified = SerializerMethodField()
    attributes = SerializerMethodField()

    class Meta:
        model = Locality
        exclude = ['domain', 'specifications', 'changeset']

    def get_location(self, obj):
        return obj.geom

    def get_date_modified(self, obj):
        return obj.changeset.created


class LocalityGeoSerializer(LocalitySerializerBase, GeoFeatureModelSerializer):
    attributes = SerializerMethodField()
    date_modified = SerializerMethodField()

    class Meta:
        model = Locality
        geo_field = 'geom'
        exclude = ['domain', 'specifications', 'changeset']

    def get_date_modified(self, obj):
        return obj.changeset.created
