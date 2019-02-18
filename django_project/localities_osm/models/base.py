__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '07/01/19'

from django.contrib.gis.db import models


class LocalityOSMBase(models.Model):
    _DATABASE = 'docker_osm'

    class Meta:
        abstract = True
