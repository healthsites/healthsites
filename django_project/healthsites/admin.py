# -*- coding: utf-8 -*-
__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '21/09/23'

from django.contrib import admin

from healthsites.models.healthsite import (
    Healthsite, HealthsiteSource
)


class HealthsiteSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'license')


class HealthsiteAdmin(admin.ModelAdmin):
    list_display = (
        'source', 'amenity', 'name', 'changeset_timestamp',
        'changeset_user', 'operator', 'administrative_code'
    )
    search_fields = ('name',)
    list_filter = ('source', 'amenity', 'administrative_code')


admin.site.register(HealthsiteSource, HealthsiteSourceAdmin)
admin.site.register(Healthsite, HealthsiteAdmin)
