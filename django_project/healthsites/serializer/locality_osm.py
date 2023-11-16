__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/12/21'

import uuid
import json
from django.contrib.gis.geos.error import GEOSException
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer, SerializerMethodField
)
from rest_framework_gis.serializers import GeoFeatureModelSerializer

from core.settings.utils import ABS_PATH
from localities_osm.models.locality import (
    LocalityOSM, LocalityOSMView,
    LocalityOSMNode, LocalityOSMWay
)
from localities_osm_extension.models.extension import LocalityOSMExtension
from localities_osm_extension.models.tag import Tag

attributes_fields = [meta_field.name for meta_field in LocalityOSM._meta.get_fields()]
attributes_fields.remove('osm_id')


class LocalityOSMBaseSerializer(object):
    key_mapping = None

    def map_tag(self, tag):
        """ return tag based on key map

        :param tag: tag that will be mapped
        :type tag: str

        :return: tag that already mapped
        :rtype: str
        """
        try:
            return self.key_mapping[tag]
        except (TypeError, KeyError):
            return tag

    def get_completeness(self, obj):
        return obj.get_completeness()

    def get_attributes(self, obj):
        """ Get attributes from model fields
        and also the extension"""
        show_all = False
        try:
            show_all = self.context.get('flat', None)

            # check tag that want to be used
            tag = self.context.get('tag_format', None)
            if tag == 'hxl':
                mapping_file_path = ABS_PATH('api', 'fixtures', 'hxl_tags.json')
                self.key_mapping = json.loads(open(mapping_file_path, 'r').read())
        except (AttributeError, IOError):
            pass

        attributes = {}
        for attribute in attributes_fields:
            if getattr(obj, attribute) or show_all:
                attributes[
                    self.map_tag(attribute)] = getattr(obj, attribute)

        # check attributes from extension
        extension, created = LocalityOSMExtension.objects.get_or_create(
            osm_id=obj.osm_id,
            osm_type=self.get_osm_type(obj)
        )
        for tag in extension.tag_set.all():
            if tag.value:
                attributes[self.map_tag(tag.name)] = tag.value

        # check and create uuid
        uuid_attribute = self.map_tag('uuid')
        try:
            attributes[uuid_attribute]
        except KeyError:
            attributes[uuid_attribute] = uuid.uuid4().hex
            Tag.objects.create(
                extension=extension,
                name='uuid',
                value=attributes[uuid_attribute]
            )
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


class LocalityOSMSerializer(
    LocalityOSMBaseSerializer,
    ModelSerializer
):
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


class LocalityOSMGeoSerializer(
    LocalityOSMBaseSerializer,
    GeoFeatureModelSerializer
):
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


class LocalityOSMNodeSerializer(
    LocalityOSMBaseSerializer,
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


class LocalityOSMNodeGeoSerializer(
    LocalityOSMBaseSerializer,
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


class LocalityOSMWaySerializer(
    LocalityOSMBaseSerializer,
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


class LocalityOSMWayGeoSerializer(
    LocalityOSMBaseSerializer,
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
