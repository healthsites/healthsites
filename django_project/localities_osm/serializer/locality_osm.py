__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '22/01/19'

from rest_framework.serializers import (
    ModelSerializer
)
from rest_framework_gis.serializers import GeometrySerializerMethodField
from localities_osm.models.locality import (
    LocalityOSMView,
    LocalityOSMNode
)


class LocalityHealthsitesOSMSerializer(ModelSerializer):
    geometry = GeometrySerializerMethodField

    class Meta:
        model = LocalityOSMView
        exclude = []

    def get_geometry(self, obj):
        return obj.geometry.centroid

    def to_representation(self, instance):
        result = super(LocalityHealthsitesOSMSerializer, self).to_representation(instance)
        clean_result = {}
        for key, value in result.items():
            if value:
                clean_result[key] = value
        return result


class LocalityHealthsitesOSMNodeSerializer(LocalityHealthsitesOSMSerializer):
    class Meta:
        model = LocalityOSMNode
        exclude = []


class LocalityOSMBasic(ModelSerializer):
    class Meta:
        model = LocalityOSMView
        fields = ['row', 'osm_id', 'osm_type', 'type', 'name', 'changeset_version', 'changeset_timestamp', 'changeset_user']
