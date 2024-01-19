__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '22/02/23'

from django.contrib import admin
from django.utils.safestring import mark_safe

from api.models.user_api_key import (
    UserApiKey, ApiKeyRequestLog, ApiKeyAccess, ApiKeyEnrollment
)


class UserApiKeyAdmin(admin.ModelAdmin):
    list_display = ('user', 'api_key', 'is_active')
    list_filter = ('api_key',)


class ApiKeyAccessAdmin(admin.ModelAdmin):
    list_display = ('api_key', 'date', 'counter')
    list_filter = ('api_key__api_key',)


class ApiKeyRequestLogAdmin(admin.ModelAdmin):
    list_display = ('api_key', 'time', 'url')
    list_filter = ('api_key__api_key',)


class ApiKeyEnrollmentAdmin(admin.ModelAdmin):
    list_display = (
        'contact_person', 'contact_email', 'organisation_name',
        'organisation_url', 'project_url', 'time', 'approved',
        '_api_key'
    )
    list_editable = ('approved',)

    def _api_key(self, obj: ApiKeyEnrollment):
        """Return colors that palette has."""
        return mark_safe(
            f'<a href="/admin/api/userapikey/{obj.api_key}/change/">'
            f'{obj.api_key}'
            f'</a>'
        )

    _api_key.allow_tags = True


admin.site.register(UserApiKey, UserApiKeyAdmin)
admin.site.register(ApiKeyAccess, ApiKeyAccessAdmin)
admin.site.register(ApiKeyRequestLog, ApiKeyRequestLogAdmin)
admin.site.register(ApiKeyEnrollment, ApiKeyEnrollmentAdmin)
