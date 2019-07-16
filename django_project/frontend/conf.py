from django.conf import settings as django_settings


class LazySettings(object):
    @property
    def GRUNT_MODULES(self):
        return getattr(django_settings, 'GRUNT_MODULES', {})

    @property
    def REQUIRED_JS_PATH(self):
        return getattr(django_settings, 'REQUIRE_JS_PATH', {})


settings = LazySettings()
