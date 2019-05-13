__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '22/01/19'

import json
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField
)
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from localities_osm.models.locality import LocalityOSM, LocalityOSMView
from localities_osm_extension.models.extension import LocalityOSMExtension

attributes_fields = LocalityOSM._meta.get_all_field_names()
attributes_fields.remove('osm_id')


class LocalityOSMBaseSerializer(object):
    def get_completeness(self, obj):
        return obj.get_completeness()

    def get_attributes(self, obj):
        attributes = {}
        for attribute in attributes_fields:
            if getattr(obj, attribute):
                attributes[attribute] = getattr(obj, attribute)
        try:
            extension = LocalityOSMExtension.objects.get(
                osm_id=obj.osm_id,
                osm_type=obj.osm_type
            )
            for tag in extension.tag_set.all():
                if tag.value:
                    attributes[tag.name] = tag.value
        except LocalityOSMExtension.DoesNotExist:
            pass
        return attributes

    def get_centroid(self, obj):
        return json.loads(obj.geometry.centroid.geojson)


class LocalityOSMSerializer(LocalityOSMBaseSerializer,
                            ModelSerializer):
    attributes = SerializerMethodField()
    centroid = SerializerMethodField()
    completeness = SerializerMethodField()

    class Meta:
        model = LocalityOSMView
        fields = ['attributes', 'centroid', 'osm_id', 'osm_type', 'completeness']


class LocalityOSMGeoSerializer(LocalityOSMBaseSerializer,
                               GeoFeatureModelSerializer):
    attributes = SerializerMethodField()
    centroid = SerializerMethodField()
    completeness = SerializerMethodField()

    class Meta:
        model = LocalityOSMView
        geo_field = 'geometry'
        fields = ['attributes', 'centroid', 'osm_id', 'osm_type', 'completeness']


class LocalityOSMBasicSerializer(ModelSerializer):
    uuid = serializers.SerializerMethodField()

    def get_uuid(self, obj):
        return '%s/%s' % (obj.osm_type, obj.osm_id)

    class Meta:
        model = LocalityOSMView
        fields = ['uuid', 'osm_id', 'osm_type',
                  'healthcare', 'name', 'changeset_version',
                  'changeset_timestamp', 'changeset_user']


class LocalityOSMProfileSerializer(ModelSerializer):
    changeset__social_user__username = serializers.SerializerMethodField()
    nickname = serializers.SerializerMethodField()
    locality_id = serializers.SerializerMethodField()
    changeset__created = serializers.SerializerMethodField()
    edit_count = serializers.SerializerMethodField()

    class Meta:
        model = LocalityOSMView
        fields = [
            'pk',
            'osm_id',
            'name',
            'changeset_id',
            'changeset_version',
            'changeset_timestamp',
            'changeset_user',
            'changeset__social_user__username',
            'nickname',
            'locality_id',
            'changeset__created',
            'edit_count'
        ]

    def get_changeset__social_user__username(self, instance):
        return None

    def get_nickname(self, instance):
        return instance.changeset_user

    def get_locality_id(self, instance):
        return None

    def get_changeset__created(self, instance):
        return instance.changeset_timestamp

    def get_edit_count(self, instance):
        return 1


class LocalityOSMAutoCompleteSerializer(ModelSerializer):
    label = SerializerMethodField()
    id = SerializerMethodField()

    class Meta:
        model = LocalityOSMView
        fields = ['label', 'id']

    def get_label(self, instance):
        return instance.name

    def get_id(self, instance):
        return '%s/%s' % (instance.osm_type, instance.osm_id)
