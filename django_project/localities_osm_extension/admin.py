# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '26/04/19'

from django.contrib import admin
from .models.extension import LocalityOSMExtension
from .models.tag import Tag
from .models.pending_state import PendingUpdate


class TagInline(admin.TabularInline):
    model = Tag


class PendingStateInline(admin.TabularInline):
    model = PendingUpdate


class LocalityOSMExtensionAdmin(admin.ModelAdmin):
    list_display = ('osm_id', 'osm_type')
    list_filter = ('osm_type',)
    search_fields = ['osm_id']
    ordering = ('osm_id', 'osm_type',)

    inlines = [TagInline, PendingStateInline]


admin.site.register(LocalityOSMExtension, LocalityOSMExtensionAdmin)
