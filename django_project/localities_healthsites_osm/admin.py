__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '22/01/19'

from django.contrib import admin
from localities_healthsites_osm.models.locality_healthsites_osm import (
    LocalityHealthsitesOSM
)
from api.serializer.locality import LocalitySerializer
from localities_osm.serializer.locality_osm import (
    LocalityHealthsitesOSMSerializer
)


class LocalityHealthsitesOSMAdmin(admin.ModelAdmin):
    list_display = ('id', 'locality_osm', 'osm_type')
    list_filter = ('osm_type',)
    search_fields = ('osm_id',)
    readonly_fields = ('osm_id', 'osm_type', 'osm_pk', 'osm_data')
    filter_horizontal = ('custom_tag', )

    def osm_data(self, obj):
        osm = obj.return_osm_view()
        if osm:
            return LocalityHealthsitesOSMSerializer(osm).data
        return None

    def locality_osm(self, obj):
        return (
                '<a href="/admin/localities_osm/localityosmview/%s">%s</a> '
                % (obj.osm_id, obj.osm_id)
        )

    locality_osm.allow_tags = True


admin.site.register(LocalityHealthsitesOSM, LocalityHealthsitesOSMAdmin)
