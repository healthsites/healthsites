__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '22/01/19'

from rest_framework.serializers import (
    ModelSerializer
)
from localities_osm.models.locality import (
    LocalityOSMView
)


class LocalityHealthsitesOSMSerializer(ModelSerializer):
    class Meta:
        model = LocalityOSMView
        exclude = []

    def get_geometry(self, obj):
        return obj.geometry

    def to_representation(self, instance):
        result = super(LocalityHealthsitesOSMSerializer, self).to_representation(instance)
        return result
