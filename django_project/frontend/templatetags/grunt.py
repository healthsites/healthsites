from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.contrib.staticfiles.storage import staticfiles_storage
from frontend.conf import settings as grunt_settings

register = template.Library()


@register.simple_tag
def grunt_module(module):
    """
    Render A Javascript based on grunt
    :param module:Script filename of js
    :return: Template to render
    """
    if not settings.DEBUG:
        return mark_safe(
            """<script type="text/javascript"
            src={optimized}></script>""".format(
                optimized=staticfiles_storage.url(
                        grunt_settings.GRUNT_MODULES[module]["optimized"]),
            )
        )

    return mark_safe(
        """<script data-main={main} src={requirejs}></script>""".format(
            main=staticfiles_storage.url(
                    grunt_settings.GRUNT_MODULES[module]["main"]),
            requirejs=grunt_settings.REQUIRED_JS_PATH
        )
    )
