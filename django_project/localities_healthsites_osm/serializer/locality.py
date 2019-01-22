__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '22/01/19'

from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField
)
from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer, GeometrySerializerMethodField, )
from localities_healthsites_osm.models import LocalityHealthsitesOSM
from localities_osm.models.locality import (
    LocalityOSMView
)
from api.serializer.locality import LocalitySerializer

attributes_fields = [
    'emergency', 'operator', 'opening_hours',
    'contact_website', 'contact_phone', 'phone',
    'website', 'speciality'
]


class LocalityHealthsitesOSMBaseSerializer(object):
    def get_attributes(self, obj):
        attributes = {}
        for attribute in attributes_fields:
            attributes[attribute] = getattr(obj, attribute)
        return attributes

    def get_healthsites_data(self, healthsite_osm):
        try:
            locality_healthsites_osm = LocalityHealthsitesOSM.objects.get(
                osm_id=healthsite_osm.osm_id,
                osm_type=healthsite_osm.osm_type
            )
            data = LocalitySerializer(locality_healthsites_osm.healthsite).data
            del data['geom']
            del data['id']
            return data
        except LocalityHealthsitesOSM.DoesNotExist:
            return {}


class LocalityHealthsitesOSMSerializer(LocalityHealthsitesOSMBaseSerializer,
                                       ModelSerializer):
    geometry = GeometrySerializerMethodField
    attributes = SerializerMethodField()

    class Meta:
        model = LocalityOSMView
        exclude = attributes_fields

    def get_geometry(self, obj):
        return obj.geometry

    def to_representation(self, instance):
        result = super(LocalityHealthsitesOSMSerializer, self).to_representation(instance)
        locality_data = self.get_healthsites_data(instance)
        attributes = result['attributes']
        result.update(locality_data)
        result['attributes'].update(attributes)
        return result


class LocalityHealthsitesOSMGeoSerializer(LocalityHealthsitesOSMBaseSerializer,
                                          GeoFeatureModelSerializer):
    attributes = SerializerMethodField()

    class Meta:
        model = LocalityOSMView
        geo_field = 'geometry'
        exclude = attributes_fields
