# -*- coding: utf-8 -*-
from django.contrib import admin
from localities_osm.models.locality import (
    LocalityOSMNode,
    LocalityOSMWay,
    LocalityOSMView
)
from localities_osm.models.locality_osm_extension import LocalityOSMExtension
from localities_osm.models.tag import Tag


class LocalityOSMAdmin(admin.ModelAdmin):
    list_display = ('osm_id', 'category', 'name', 'changeset_timestamp', 'changeset_user')
    list_filter = ('type',)
    ordering = ('name',)
    search_fields = ('name', 'osm_id')
    readonly_fields = ('osm_id',)


class LocalityOSMViewAdmin(LocalityOSMAdmin):
    list_display = (
        'osm_id', 'category', 'name', 'osm_type', 'changeset_timestamp', 'changeset_user')
    list_filter = ('category', 'osm_type')
    readonly_fields = ('osm_id', 'row', 'osm_type')


admin.site.register(LocalityOSMWay, LocalityOSMAdmin)
admin.site.register(LocalityOSMNode, LocalityOSMAdmin)
admin.site.register(LocalityOSMView, LocalityOSMViewAdmin)
admin.site.register(LocalityOSMExtension)
admin.site.register(Tag)
