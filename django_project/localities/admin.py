# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import (
    Country, DataLoader, DataLoaderPermission
)


class DataLoaderAdmin(admin.ModelAdmin):
    list_display = (
        'author', 'date_time_uploaded', 'applied', 'date_time_applied', 'notes'
    )

    def has_add_permission(self, request):
        return False


admin.site.register(DataLoader, DataLoaderAdmin)


class DataLoaderPermissionAdmin(admin.ModelAdmin):
    list_display = (
        'uploader', 'accepted_csv',)


admin.site.register(DataLoaderPermission, DataLoaderPermissionAdmin)


class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'parent')
    fields = ('name', 'code', 'parent')
    readonly_fields = ('code', 'parent')
    ordering = ('name',)
    search_fields = ('name', 'code')


admin.site.register(Country, CountryAdmin)
