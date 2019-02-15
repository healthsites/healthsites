__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '22/01/19'

from django.contrib import admin
from localities_healthsites_osm.models.locality_healthsites_osm import (
    LocalityHealthsitesOSM
)
from api.serializer.locality import LocalitySerializer
from localities_osm.models.locality import LocalityOSMView, LocalityOSMNode
from localities_osm.serializer.locality_osm import (
    LocalityHealthsitesOSMSerializer,
    LocalityHealthsitesOSMNodeSerializer
)


class LocalityHealthsitesOSMAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'locality_healthsite', 'locality_osm', 'osm_type')
    ordering = ('healthsite',)
    list_filter = ('osm_type',)
    search_fields = ('healthsite__name', 'osm_id')
    readonly_fields = ('healthsite', 'osm_id', 'osm_type', 'osm_pk', 'healthsite_data', 'osm_data')

    def healthsite_data(self, obj):
        return LocalitySerializer(obj.healthsite).data

    def osm_data(self, obj):
        try:
            osm = LocalityOSMView.objects.get(
                osm_id=obj.osm_id,
                osm_type=obj.osm_type
            )
            return LocalityHealthsitesOSMSerializer(osm).data
        except LocalityOSMView.DoesNotExist:
            try:
                if obj.pk:
                    osm = LocalityOSMNode.objects.get(
                        pk=obj.osm_pk
                    )
                    data = LocalityHealthsitesOSMNodeSerializer(osm).data
                    return data
            except LocalityOSMNode.DoesNotExist:
                pass
            except Exception as e:
                pass
        return '-'

    def locality_healthsite(self, obj):
        return (
                '<a href="/admin/localities/locality/%s">%s</a> ' % (
            obj.healthsite.id, obj.healthsite.name
        )
        )

    def locality_osm(self, obj):
        return (
                '<a href="/admin/localities_osm/localityosmview/%s">%s</a> ' % (
            obj.osm_id, obj.osm_id
        )
        )

    locality_healthsite.allow_tags = True
    locality_osm.allow_tags = True


admin.site.register(LocalityHealthsitesOSM, LocalityHealthsitesOSMAdmin)
