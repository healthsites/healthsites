__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '22/01/19'

import json
from django.db.models import Q
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
)
from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer, GeometrySerializerMethodField, )
from localities_healthsites_osm.models.locality_healthsites_osm import (
    LocalityHealthsitesOSM
)
from localities_osm.models.locality import (
    LocalityOSMView, LocalityOSM
)
from api.serializer.locality import LocalitySerializer

attributes_fields = LocalityOSM._meta.get_all_field_names()
attributes_fields.remove('osm_id')


class LocalityHealthsitesOSMBaseSerializer(object):
    def get_attributes(self, obj):
        attributes = {}
        for attribute in attributes_fields:
            attributes[attribute] = getattr(obj, attribute)
        return attributes

    def get_healthsites_data(self, healthsite_osm):
        try:
            locality_healthsites_osm = LocalityHealthsitesOSM.objects.get(
                Q(osm_id=healthsite_osm.osm_id,
                  osm_type=healthsite_osm.osm_type) | Q(osm_pk=healthsite_osm.row.split('-')[0])
            )
            data = LocalitySerializer(locality_healthsites_osm.healthsite).data
        except LocalityHealthsitesOSM.DoesNotExist:
            return {}
        del data['geom']
        del data['id']
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
                    result['attributes']['staff'][key] = value
                if key == 'full_time_beds':
                    result['attributes']['inpatient_service'][key] = value
                else:
                    result['attributes'][key] = value
        result['geometry'] = json.loads(self.get_geometry(instance).geojson)
        return result


class LocalityHealthsitesOSMGeoSerializer(LocalityHealthsitesOSMBaseSerializer,
                                          GeoFeatureModelSerializer):
    attributes = SerializerMethodField()

    class Meta:
        model = LocalityOSMView
        geo_field = 'geometry'
        exclude = attributes_fields
