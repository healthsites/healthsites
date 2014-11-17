# -*- coding: utf-8 -*-
import logging
LOG = logging.getLogger(__name__)

import math

from .models import Locality


def within_bbox(bbox, geomx, geomy):
    if bbox[0] < geomx < bbox[2] and bbox[1] < geomy < bbox[3]:
        return True
    else:
        return False


def overlapping_area(zoom, pix_x, pix_y, lat):
    C = (2 * 6378137.0 * math.pi) / 256.  # one pixel
    C2 = (2 * 6378137.0 * math.pi) / 360.  # one degree

    lat_deformation = (C * math.cos(math.radians(lat)) / 2 ** zoom)

    lat_deg = (lat_deformation * pix_y) / C2
    lng_deg = (lat_deformation * pix_x) / C2

    return (lat_deg, lng_deg)


def cluster(zoom, pix_x, pix_y):
    cluster_points = []

    localites = (
        Locality.objects
        .extra(select={'xy': 'st_x(geom)||$$,$$||st_y(geom)'})
        .values('id', 'xy')
    )

    for locality in localites.iterator():
        geomx, geomy = map(float, locality['xy'].split(','))
        for pt in cluster_points:
            if within_bbox(pt['bbox'], geomx, geomy):
                pt['count'] += 1
                break

        else:
            x_range, y_range = overlapping_area(zoom, pix_x, pix_y, geomy)

            bbox = (
                geomx - x_range/1.5, geomy - y_range/1.5,
                geomx + x_range/1.5, geomy + y_range/1.5
            )
            cluster_points.append({
                'id': locality['id'],
                'count': 1,
                'geom': (geomx, geomy),
                'bbox': bbox
            })

    return cluster_points
