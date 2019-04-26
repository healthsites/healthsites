# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '26/04/19'

from django.contrib import admin
from .models.locality_osm_extension import LocalityOSMExtension
from .models.tag import Tag

admin.site.register(LocalityOSMExtension)
admin.site.register(Tag)
