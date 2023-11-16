__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '21/09/23'

from django.contrib.gis.db import models


class Amenity(models.TextChoices):
    """Amenity types."""

    CLINIC = 'clinic'
    DOCTORS = 'doctors'
    HOSPITAL = 'hospital'
    DENTIST = 'dentist'
    PHARMACY = 'pharmacy'


class Healthcare(models.TextChoices):
    """Healthcare types."""

    DOCTOR = 'doctor'
    PHARMACY = 'pharmacy'
    HOSPITAL = 'hospital'
    CLINIC = 'clinic'
    DENTIST = 'dentist'
    PHYSIOTHERAPIST = 'physiotherapist'
    ALTERNATIVE = 'alternative'
    LABORATORY = 'laboratory'
    OPTOMETRIST = 'optometrist'
    REHABILITATION = 'rehabilitation'
    BLOOD_DONATION = 'blood_donation'
    BIRTHING_CENTER = 'birthing_center'
