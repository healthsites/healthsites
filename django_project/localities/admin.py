# -*- coding: utf-8 -*-
from django.contrib import admin

from masterization import promote_unconfirmed_synonym, reject_unconfirmed_synonym

from .forms import DomainModelForm
from .models import (
    Attribute, Changeset, Country, DataLoader, DataLoaderPermission,
    Domain, Locality, Specification, SynonymLocalities, UnconfirmedSynonym
)


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
        'organisation_name', 'author', 'data_loader_mode', 'date_time_uploaded', 'applied',
        'date_time_applied'
    )

    def has_add_permission(self, request):
        return False


admin.site.register(DataLoader, DataUpdateAdmin)


class DataLoaderPermissionAdmin(admin.ModelAdmin):
    list_display = (
        'uploader', 'accepted_csv',)


admin.site.register(DataLoaderPermission, DataLoaderPermissionAdmin)


class LocalityAdmin(admin.ModelAdmin):
    list_display = (
        'upstream_id', 'locality_uuid', 'name', 'locality_location', 'is_master',)
    readonly_fields = (
        'upstream_id', 'locality_uuid', 'source', 'name', 'core_field', 'locality_location',
        'is_master'
    )
    fieldsets = (
        ('Masterization', {
            'fields': (
                'is_master',),
        }),
        ('Mandatory Attribute', {
            'fields': (
                'upstream_id',
                'locality_uuid',
                'name',
                'source',
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

    def core_field(self, obj):
        output = ""
        if obj:
            dict = obj.repr_dict()
            if "values" in dict:
                for key in sorted(dict["values"].keys()):
                    value = dict['values'][key]
                    value = value.replace("|", ",")
                    show = True
                    test_value = value.replace("-", "").replace(",", "")
                    if key == "defining_hours" and len(test_value) == 0:
                        show = False
                    elif len(value.replace(",", "")) == 0:
                        show = False
                    if show:
                        row = "<b>%s</b> : <a>%s</a></br>" % (
                            key.replace("_", " "), dict['values'][key]
                        )
                        output += row

        return output

    def has_add_permission(self, request):
        return False

    locality_uuid.allow_tags = True
    core_field.allow_tags = True


admin.site.register(Locality, LocalityAdmin)


class SynonymLocalitiesAdmin(admin.ModelAdmin):
    list_display = ('id', 'master', 'the_synonym')
    readonly_fields = ('id', 'master', 'the_synonym')
    fieldsets = (
        (None, {
            'fields': (
                'master',
                'the_synonym',),
        }),
    )

    def master(self, obj):
        return (
            '<a href="/admin/localities/locality/%s">%s</a> '
            '(<a href="/map#!/locality/%s">%s</a>)' % (
                obj.locality.id, obj.locality.name, obj.locality.uuid, obj.locality.uuid
            )
        )

    def the_synonym(self, obj):
        return (
            '<a href="/admin/localities/locality/%s">%s</a> '
            '(<a href="/map#!/locality/%s">%s</a>)' % (
                obj.synonym.id, obj.synonym.name, obj.synonym.uuid, obj.synonym.uuid
            )
        )

    master.short_description = 'Master'
    master.admin_order_field = 'locality__uuid'
    the_synonym.short_description = 'Synonym'
    the_synonym.admin_order_field = 'synonyms__uuid'
    master.allow_tags = True
    the_synonym.allow_tags = True


admin.site.register(SynonymLocalities, SynonymLocalitiesAdmin)


def promote_potential_synonyms(modeladmin, request, queryset):
    for unconfirmed_synonym in queryset:
        promote_unconfirmed_synonym(unconfirmed_synonym.id)


def reject_potential_synonyms(modeladmin, request, queryset):
    for unconfirmed_synonym in queryset:
        reject_unconfirmed_synonym(unconfirmed_synonym.id)


class UnconfirmedSynonymAdmin(admin.ModelAdmin):
    list_display = ('id', 'master', 'potential_synonym')
    readonly_fields = ('id', 'master', 'potential_synonym')
    fieldsets = (
        (None, {
            'fields': (
                'master',
                'potential_synonym',),
        }),
    )
    actions = [promote_potential_synonyms, reject_potential_synonyms]

    def master(self, obj):
        return (
            '<a href="/admin/localities/locality/%s">%s</a> '
            '(<a href="/map#!/locality/%s">%s</a>)' % (
                obj.locality.id, obj.locality.name, obj.locality.uuid, obj.locality.uuid
            )
        )

    def potential_synonym(self, obj):
        return (
            '<a href="/admin/localities/locality/%s">%s</a> '
            '(<a href="/map#!/locality/%s">%s</a>)' % (
                obj.synonym.id, obj.synonym.name, obj.synonym.uuid, obj.synonym.uuid
            )
        )

    master.short_description = 'Master'
    master.admin_order_field = 'locality__uuid'
    potential_synonym.admin_order_field = 'synonyms__uuid'
    promote_potential_synonyms.short_description = "Promote selected localities as synonyms"
    reject_potential_synonyms.short_description = "Reject selected localities as synonyms"
    master.allow_tags = True
    potential_synonym.allow_tags = True


admin.site.register(UnconfirmedSynonym, UnconfirmedSynonymAdmin)


class CountryAdmin(ChangesetMixin, admin.ModelAdmin):
    fields = ('name',)
    ordering = ('name',)
    search_fields = ('name',)


admin.site.register(Country, CountryAdmin)
