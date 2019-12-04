__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '22/01/19'

import uuid
import json
from django.contrib.gis.geos.error import GEOSException
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField
)
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from localities_osm.models.locality import (
    LocalityOSM, LocalityOSMView,
    LocalityOSMNode, LocalityOSMWay
)
from localities_osm_extension.models.extension import LocalityOSMExtension
from localities_osm_extension.models.tag import Tag

attributes_fields = LocalityOSM._meta.get_all_field_names()
attributes_fields.remove('osm_id')


class LocalityOSMBaseSerializer(object):
    def get_completeness(self, obj):
        return obj.get_completeness()

    def get_attributes(self, obj):
        """ Get attributes from model fields
        and also the extension"""
        show_all = False
        try:
            show_all = self.context.get('flat', None)
        except AttributeError:
            pass

        attributes = {}
        for attribute in attributes_fields:
            if getattr(obj, attribute) or show_all:
                attributes[attribute] = getattr(obj, attribute)

        extension = None
        osm_id = obj.osm_id
        osm_type = self.get_osm_type(obj)
        try:
            extension = LocalityOSMExtension.objects.get(
                osm_id=osm_id,
                osm_type=osm_type
            )
            for tag in extension.tag_set.all():
                if tag.value:
                    attributes[tag.name] = tag.value
        except LocalityOSMExtension.DoesNotExist:
            pass

        try:
            attributes['uuid']
        except KeyError:
            locality_uuid = uuid.uuid4().hex
            if not extension:
                extension, created = LocalityOSMExtension.objects.get_or_create(
                    osm_id=osm_id,
                    osm_type=osm_type
                )
            Tag.objects.create(
                extension=extension,
                name='uuid',
                value=locality_uuid
            )
            attributes['uuid'] = locality_uuid
        return attributes

    def get_centroid(self, obj):
        if obj.geometry:
            try:
                return json.loads(obj.geometry.centroid.geojson)
            except GEOSException:
                return None
        else:
            return None

    def get_osm_type(self, obj):
        return obj.osm_type


class LocalityOSMSerializer(LocalityOSMBaseSerializer,
                            ModelSerializer):
    attributes = SerializerMethodField()
    centroid = SerializerMethodField()
    completeness = SerializerMethodField()

    class Meta:
        model = LocalityOSMView
        fields = ['attributes', 'centroid', 'osm_id', 'osm_type', 'completeness']

    def to_representation(self, instance):
        result = super(LocalityOSMSerializer, self).to_representation(instance)
        if self.context.get('flat', None):
            result.update(result['attributes'])
            del result['attributes']
            del result['centroid']
        return result


class LocalityOSMGeoSerializer(LocalityOSMBaseSerializer,
                               GeoFeatureModelSerializer):
    attributes = SerializerMethodField()
    centroid = SerializerMethodField()
    completeness = SerializerMethodField()

    class Meta:
        model = LocalityOSMView
        geo_field = 'geometry'
        fields = ['attributes', 'centroid', 'osm_id', 'osm_type', 'completeness']

    def to_representation(self, instance):
        result = super(LocalityOSMGeoSerializer, self).to_representation(instance)
        if self.context.get('flat', None):
            result['properties'].update(result['properties']['attributes'])
            del result['properties']['attributes']
            del result['properties']['centroid']
        return result


class LocalityOSMNodeSerializer(LocalityOSMBaseSerializer,
                                ModelSerializer):
    attributes = SerializerMethodField()
    centroid = SerializerMethodField()
    completeness = SerializerMethodField()
    osm_type = SerializerMethodField()

    def get_osm_type(self, obj):
        return 'node'

    class Meta:
        model = LocalityOSMNode
        fields = ['attributes', 'centroid', 'osm_id', 'osm_type', 'completeness']


class LocalityOSMNodeGeoSerializer(LocalityOSMBaseSerializer,
                                   GeoFeatureModelSerializer):
    attributes = SerializerMethodField()
    centroid = SerializerMethodField()
    completeness = SerializerMethodField()
    osm_type = SerializerMethodField()

    def get_osm_type(self, obj):
        return 'node'

    class Meta:
        model = LocalityOSMNode
        geo_field = 'geometry'
        fields = ['attributes', 'centroid', 'osm_id', 'osm_type', 'completeness']


class LocalityOSMWaySerializer(LocalityOSMBaseSerializer,
                               ModelSerializer):
    attributes = SerializerMethodField()
    centroid = SerializerMethodField()
    completeness = SerializerMethodField()
    osm_type = SerializerMethodField()

    def get_osm_type(self, obj):
        return 'way'

    class Meta:
        model = LocalityOSMWay
        fields = ['attributes', 'centroid', 'osm_id', 'osm_type', 'completeness']


class LocalityOSMWayGeoSerializer(LocalityOSMBaseSerializer,
                                  GeoFeatureModelSerializer):
    attributes = SerializerMethodField()
    centroid = SerializerMethodField()
    completeness = SerializerMethodField()
    osm_type = SerializerMethodField()

    def get_osm_type(self, obj):
        return 'way'

    class Meta:
        model = LocalityOSMWay
        geo_field = 'geometry'
        fields = ['attributes', 'centroid', 'osm_id', 'osm_type', 'completeness']


class LocalityOSMBasicSerializer(ModelSerializer):
    uuid = serializers.SerializerMethodField()
    name = serializers.SerializerMethodField()

    def get_name(self, obj):
        if obj.name:
            return obj.name
        else:
            return '<i>No Name</i>'

    def get_uuid(self, obj):
        return '%s/%s' % (obj.osm_type, obj.osm_id)

    class Meta:
        model = LocalityOSMView
        fields = ['uuid', 'osm_id', 'osm_type',
                  'healthcare', 'name', 'changeset_version',
                  'changeset_timestamp', 'changeset_user']


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
