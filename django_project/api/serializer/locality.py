__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '29/11/18'

from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField)
from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer, GeometrySerializerMethodField)
from localities.models import Locality


class LocalitySerializer(ModelSerializer):
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

    def get_attributes(self, obj):
        dict = obj.repr_dict(clean=True)
        return dict['values']


class LocalityGeoSerializer(GeoFeatureModelSerializer):
    attributes = SerializerMethodField()
    date_modified = SerializerMethodField()

    class Meta:
        model = Locality
        geo_field = 'geom'
        exclude = ['domain', 'specifications', 'changeset']

    def get_date_modified(self, obj):
        return obj.changeset.created

    def get_attributes(self, obj):
        dict = obj.repr_dict(clean=True)
        return dict['values']
