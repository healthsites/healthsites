__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/02/19'

from rest_framework import serializers

NATURE_OF_FACILITY_CHOICES = [
    "clinic without beds",
    "clinic with beds",
    "first referral hospital",
    "second referral hospital or General hospital",
    "tertiary level including University hospital"
]
OWNERSHIP_CHOICES = [
    "public",
    "private not for profit",
    "private commercial"
]
ACTIVITIES_CHOICES = [
    "medicine and medical specialties",
    "surgery and surgical specialties",
    "Maternal and women health",
    "pediatric care"
]
ANCILLARY_SERVICES_CHOICES = [
    "Operating theater",
    "laboratory",
    "imaging equipment",
    "intensive care unit"
]
SCOPE_OF_SERVICE_CHOICES = [
    "specialized care",
    "general acute care",
    "rehabilitation care",
    "old age/hospice care"
]


class LocalityPostSerializer(serializers.Serializer):
    """ This is locality serializer for post body"""
    name = serializers.CharField(max_length=512, help_text="Locality name")
    latitude = serializers.FloatField(help_text="Latitude position of healthsite")
    longitude = serializers.FloatField(help_text="Longitude position of healthsite")
    nature_of_facility = serializers.ChoiceField(
        choices=NATURE_OF_FACILITY_CHOICES, required=False, help_text="nature of facility for this healthsite")
    ownership = serializers.ChoiceField(
        choices=OWNERSHIP_CHOICES, required=False, help_text="ownership for this healthsite")

    activities = serializers.MultipleChoiceField(
        choices=ACTIVITIES_CHOICES, required=False,
        help_text="Activity for this healthsite. Valid choices are %s" % ACTIVITIES_CHOICES)
    ancillary_services = serializers.MultipleChoiceField(
        choices=ANCILLARY_SERVICES_CHOICES, required=False,
        help_text="Ancillary services for this healthsite. Valid choices are %s" % ANCILLARY_SERVICES_CHOICES)
    scope_of_service = serializers.MultipleChoiceField(
        choices=SCOPE_OF_SERVICE_CHOICES, required=False,
        help_text="Scope of services for this healthsite. Valid choices are %s" % SCOPE_OF_SERVICE_CHOICES)
    full_time_beds = serializers.IntegerField(required=False, help_text="Number of full time bed")
    part_time_beds = serializers.IntegerField(required=False, help_text="Number of part time bed")
    nurses = serializers.IntegerField(required=False, help_text="Number of nurses")
    doctors = serializers.IntegerField(required=False, help_text="Number of doctors")
    sunday = serializers.ListField(required=False, help_text="Sunday opening hours")
    monday = serializers.ListField(required=False, help_text="Monday opening hours")
    tuesday = serializers.ListField(required=False, help_text="Tuesday opening hours")
    wednesday = serializers.ListField(required=False, help_text="Wednesday opening hours")
    thursday = serializers.ListField(required=False, help_text="Thursday opening hours")
    friday = serializers.ListField(required=False, help_text="Friday opening hours")
    saturday = serializers.ListField(required=False, help_text="Saturday opening hours")
