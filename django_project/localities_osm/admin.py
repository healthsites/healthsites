# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/12/21'

from django.contrib import admin
from localities_osm.models.locality import (
    LocalityOSMNode,
    LocalityOSMWay,
    LocalityOSMView
)


class LocalityOSMAdmin(admin.ModelAdmin):
    list_display = (
        'osm_id', 'amenity', 'name', 'changeset_timestamp', 'changeset_user', 'administrative_code')
    list_filter = ('administrative_code',)
    ordering = ('name',)
    search_fields = ('name', 'osm_id')
    readonly_fields = ('osm_id',)


class LocalityOSMViewAdmin(LocalityOSMAdmin):
    list_display = (
        'osm_id', 'amenity', 'name', 'osm_type', 'changeset_timestamp',
        'changeset_user', 'operator', 'administrative_code')
    list_filter = ('amenity', 'osm_type', 'administrative_code')
    readonly_fields = ('osm_id', 'row', 'osm_type')


admin.site.register(LocalityOSMWay, LocalityOSMAdmin)
admin.site.register(LocalityOSMNode, LocalityOSMAdmin)
admin.site.register(LocalityOSMView, LocalityOSMViewAdmin)
