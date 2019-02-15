# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('localities_osm', '0002_osm_facilities_view'),
    ]

    sql = """
    CREATE VIEW osm_healthcare_facilities AS 
    select concat(id,'-node') as row, 'node' as osm_type, * from osm_healthcare_facilities_node UNION 
    select concat(id,'-way') as row, 'way' AS osm_type, * from osm_healthcare_facilities_way;
    """

    operations = [
        migrations.RunSQL('DROP VIEW IF EXISTS osm_healthcare_facilities;'),
        migrations.RunSQL(sql)
    ]
