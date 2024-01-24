__author__ = 'Irwan Fathurrahman <meomancer@gmail.com>'
__date__ = '20/12/21'

from django.contrib.gis.db import models


class LocalityOSMBase(models.Model):
    _DATABASE = 'docker_osm'

    class Meta:
        abstract = True
