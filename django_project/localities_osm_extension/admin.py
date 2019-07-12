# coding=utf-8
__author__ = 'Anita Hapsari <anita@kartoza.com>'
__date__ = '26/04/19'

from django.contrib import admin
from .models.extension import LocalityOSMExtension
from .models.tag import Tag
from .models.pending_state import PendingUpdate, PendingReview


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


class PendingUpdateAdmin(admin.ModelAdmin):
    list_display = ('extension', 'uploader', 'name', 'version', 'time_uploaded')
    list_filter = ('uploader', 'time_uploaded')
    search_fields = ['name']


class PendingReviewAdmin(admin.ModelAdmin):
    list_display = ('uploader', 'name', 'reason', 'time_uploaded')
    list_filter = ('uploader', 'time_uploaded')
    search_fields = ['name']


admin.site.register(LocalityOSMExtension, LocalityOSMExtensionAdmin)
admin.site.register(PendingUpdate, PendingUpdateAdmin)
admin.site.register(PendingReview, PendingReviewAdmin)
