__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '21/09/23'

from django.contrib.gis.db import models

from healthsites.models.source import HealthsiteSource
from localities_osm.enumerate import Amenity, Healthcare
from localities_osm.models.base import LocalityOSMBase
from localities_osm.querysets import OSMManager


class Healthsite(LocalityOSMBase):
    """Healthsite that is coming from specific source other than OSM."""

    source = models.ForeignKey(
        HealthsiteSource, on_delete=models.CASCADE
    )
    amenity = models.CharField(
        max_length=512,
        help_text='amenity=clinic,doctors,hospital,dentist,pharmacy',
        choices=Amenity.choices,
        default=Amenity.HOSPITAL
    )
    healthcare = models.CharField(
        max_length=512, blank=True, null=True,
        help_text=(
            'healthcare=doctor,pharmacy,hospital,clinic,'
            'dentist,physiotherapist,alternative'
            ',laboratory,optometrist,rehabilitation,'
            'blood_donation,birthing_center'
        ),
        choices=Healthcare.choices,
        default=Healthcare.HOSPITAL
    )
    name = models.CharField(
        max_length=512
    )
    operator = models.CharField(
        max_length=512,
        blank=True,
        null=True
    )
    administrative_code = models.CharField(
        blank=True,
        null=True,
        max_length=32
    )
    attributes = models.JSONField(
        blank=True,
        null=True
    )

    # changesets
    changeset_id = models.IntegerField(
        blank=True,
        null=True
    )
    changeset_version = models.IntegerField(
        blank=True,
        null=True
    )
    changeset_timestamp = models.DateTimeField(
        blank=True,
        null=True
    )
    changeset_user = models.CharField(
        max_length=512,
        blank=True,
        null=True
    )

    objects = OSMManager()
