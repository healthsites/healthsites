"""Core admin."""
from django.contrib import admin

from core.models import SitePreferences


class SitePreferencesAdmin(admin.ModelAdmin):
    """Site Preferences admin."""

    fieldsets = (
        ('', {
            'fields': ('site_url',),
        }),
        ('API KEY', {
            'fields': ('default_max_request_api',),
        }),
    )


admin.site.register(SitePreferences, SitePreferencesAdmin)
