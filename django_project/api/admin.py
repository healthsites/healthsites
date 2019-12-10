# -*- coding: utf-8 -*-
from django.contrib import admin
from api.models.user_api_key import UserApiKey


class UserApiKeyAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'api_key', 'is_active', 'allow_write')
    ordering = ('user',)
    list_filter = ('is_active', 'allow_write')
    readonly_fields = ('api_key',)


admin.site.register(UserApiKey, UserApiKeyAdmin)
