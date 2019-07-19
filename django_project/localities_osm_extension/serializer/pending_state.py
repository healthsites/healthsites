__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '15/07/19'

import ast
import json
from django.contrib.gis.geos import Point
from rest_framework_gis.serializers import (
    GeoFeatureModelSerializer, GeometrySerializerMethodField)
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from localities_osm_extension.models.pending_state import (
    PendingReview, PendingUpdate)


class PendingReviewSerializer(ModelSerializer):
    uploader = SerializerMethodField()
    payload = SerializerMethodField()

    class Meta:
        model = PendingReview
        fields = '__all__'

    def get_uploader(self, obj):
        return obj.uploader.username

    def get_payload(self, obj):
        return ast.literal_eval(obj.payload)


class PendingReviewGeoSerializer(GeoFeatureModelSerializer):
    geom = GeometrySerializerMethodField()
    centroid = SerializerMethodField()
    attributes = SerializerMethodField()
    osm_id = SerializerMethodField()
    osm_type = SerializerMethodField()
    reason = SerializerMethodField()

    class Meta:
        model = PendingReview
        geo_field = 'geom'
        fields = ['centroid', 'attributes', 'osm_id', 'osm_type', 'reason']

    def get_payload(self, obj):
        payload = ast.literal_eval(obj.payload)
        payload['type'] = 'node'
        return payload

    def get_geom(self, obj):
        payload = self.get_payload(obj)
        return Point(payload.get('lon', None), payload.get('lat', None))

    def get_centroid(self, obj):
        return json.loads(self.get_geom(obj).geojson)

    def get_attributes(self, obj):
        payload = self.get_payload(obj)
        return payload.get('tag', {})

    def get_osm_id(self, obj):
        payload = self.get_payload(obj)
        return payload.get('id', None)

    def get_osm_type(self, obj):
        payload = self.get_payload(obj)
        return payload.get('type', 'node')

    def get_reason(self, obj):
        return obj.reason


class PendingUpdateSerializer(ModelSerializer):
    uploader = SerializerMethodField()
    osm_id = SerializerMethodField()
    osm_type = SerializerMethodField()

    class Meta:
        model = PendingUpdate
        fields = '__all__'

    def get_uploader(self, obj):
        return obj.uploader.username

    def get_osm_id(self, obj):
        return obj.extension.osm_id

    def get_osm_type(self, obj):
        return obj.extension.osm_type
