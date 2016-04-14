# -*- coding: utf-8 -*-
from django.contrib import admin
from .models import (
    Attribute,
    Changeset,
    DataLoader,
    DataLoaderPermission,
    Domain,
    Locality,
    Specification,
    Value,
)
from .forms import DomainModelForm



class ChangesetMixin():
    """
    In order to create or update any model that uses models.ChangesetMixin we
    need to override Django admin *save_model* and create a new changeset
    """

    def save_model(self, request, obj, form, change):
        tmp_chgset = Changeset()
        tmp_chgset.social_user = request.user
        tmp_chgset.save()
        obj.changeset = tmp_chgset
        obj.save()


class DomainMA(ChangesetMixin, admin.ModelAdmin):
    fields = ('name', 'description', 'template_fragment')
    form = DomainModelForm


admin.site.register(Domain, DomainMA)


class AttributeMA(ChangesetMixin, admin.ModelAdmin):
    fields = ('key', 'description')


admin.site.register(Attribute, AttributeMA)


class SpecificationMA(ChangesetMixin, admin.ModelAdmin):
    fields = ('domain', 'attribute', 'required')


admin.site.register(Specification, SpecificationMA)


class DataUpdateAdmin(admin.ModelAdmin):
    list_display = (
        'organisation_name', 'author', 'data_loader_mode', 'date_time_uploaded', 'applied', 'date_time_applied')

    def has_add_permission(self, request):
        return False


admin.site.register(DataLoader, DataUpdateAdmin)


class DataLoaderPermissionAdmin(admin.ModelAdmin):
    list_display = (
        'uploader', 'accepted_csv',)


admin.site.register(DataLoaderPermission, DataLoaderPermissionAdmin)


class LocalityAdmin(admin.ModelAdmin):
    list_display = (
        'upstream_id', 'locality_uuid', 'locality_name', 'locality_location',)
    readonly_fields = ('upstream_id', 'locality_uuid', 'core_field', 'locality_location')
    fieldsets = (
        ('Mandatory Attribute', {
            'fields': (
                'upstream_id',
                'locality_uuid',
                'locality_location',),
        }),
        (None, {
            'fields': ('core_field',),
        }),
    )
    search_fields = ('uuid', 'upstream_id',)

    def locality_uuid(self, obj):
        return '<a href="/map#!/locality/%s">%s</a>' % (obj.uuid, obj.uuid)

    def locality_location(self, obj):
        return '(%s , %s)' % (obj.geom.x, obj.geom.y)

    def locality_name(self, obj):
        try:
            name = Value.objects.filter(
                specification__attribute__key='name').get(locality=obj)
            return name.data
        except Value.DoesNotExist:
            return ""

    def core_field(self, obj):
        output = ""
        if obj:
            dict = obj.repr_dict()
            if "values" in dict:
                for key in sorted(dict["values"].keys()):
                    value = dict['values'][key]
                    value = value.replace("|", ",")
                    show = True
                    if key == "defining_hours" and len(value.replace("-", "").replace(",", "")) == 0:
                        show = False
                    elif len(value.replace(",", "")) == 0:
                        show = False
                    if show:
                        row = "<b>%s</b> : <a>%s</a></br>" % (key.replace("_", " "), dict['values'][key])
                        output += row

        return output

    def has_add_permission(self, request):
        return False

    locality_uuid.allow_tags = True
    core_field.allow_tags = True


admin.site.register(Locality, LocalityAdmin)
