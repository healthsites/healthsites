__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '22/02/23'

from django.contrib import admin

from api.models.user_api_key import UserApiKey, ApiKeyRequestLog, ApiKeyAccess


class UserApiKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'api_key', 'is_active')
    list_filter = ('api_key',)


class ApiKeyAccessAdmin(admin.ModelAdmin):
    list_display = ('api_key', 'date', 'counter')
    list_filter = ('api_key__api_key',)


class ApiKeyRequestLogAdmin(admin.ModelAdmin):
    list_display = ('api_key', 'time', 'url')
    list_filter = ('api_key__api_key',)


admin.site.register(UserApiKey, UserApiKeyAdmin)
admin.site.register(ApiKeyAccess, ApiKeyAccessAdmin)
admin.site.register(ApiKeyRequestLog, ApiKeyRequestLogAdmin)
