"""Global context that will be returned for every request."""
from core.models.preferences import SitePreferences
from core.serializer.site_preferences import SitePreferencesSerializer


def global_context(request):
    """Global context that will be returned for every request."""
    pref = SitePreferences.preferences()
    return {
        'preferences': SitePreferencesSerializer(pref).data
    }
