# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):
    dependencies = [
        ('localities_osm', '0001_initial'),
    ]

    sql = """
    CREATE VIEW osm_healthcare_facilities AS 
    select concat(osm_id,'-node') as row, 'node' as osm_type, * from osm_healthcare_facilities_node UNION 
    select concat(osm_id,'-way') as row, 'way' AS osm_type, * from osm_healthcare_facilities_way;
    """

    operations = [
        migrations.RunSQL('DROP VIEW IF EXISTS osm_healthcare_facilities;'),
        migrations.RunSQL(sql)
    ]
