__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '22/01/19'

import datetime
from rest_framework import serializers
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
        fields = ['row', 'osm_id', 'osm_type',
                  'type', 'name', 'changeset_version',
                  'changeset_timestamp', 'changeset_user']


class LocalityOSMUpdates(ModelSerializer):
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
