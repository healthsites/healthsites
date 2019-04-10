# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '10/04/19'

from rest_framework import serializers
from localities_osm.models.locality import LocalityOSMView


class LocalityOSMCentroidSerializer(serializers.ModelSerializer):
    lat = serializers.SerializerMethodField()
    lng = serializers.SerializerMethodField()

    class Meta:
        model = LocalityOSMView
        fields = [
            'lat',
            'lng'
        ]

    def get_lat(self, instance):
        lat, lon = instance.geometry.centroid.tuple
        return lat

    def get_lng(self, instance):
        lat, lon = instance.geometry.centroid.tuple
        return lon