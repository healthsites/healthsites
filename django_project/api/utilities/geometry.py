__author__ = 'Irwan Fathurrahman <irwan@kartoza.com>'
__date__ = '14/05/19'

import math
from django.contrib.gis.geos import Polygon


def parse_bbox(bbox):
    """
    Convert a textual bbox to a GEOS polygon object

    This function assumes that any raised exceptions will be handled upstream
    """

    tmp_bbox = map(float, bbox.split(','))

    if tmp_bbox[0] > tmp_bbox[2] or tmp_bbox[1] > tmp_bbox[3]:
        # bbox is not properly formatted minLng, minLat, maxLng, maxLat
        raise ValueError
    # create polygon from bbox
    return Polygon.from_bbox(tmp_bbox)


def within_bbox(bbox, geomx, geomy):
    """
    Check if a point (geomx, geomy) is within a bbox (minx, miny, maxx, maxy)
    """

    if bbox[0] < geomx < bbox[2] and bbox[1] < geomy < bbox[3]:
        return True
    else:
        return False


def overlapping_area(zoom, pix_x, pix_y, lat):
    """
    Calculate an area (lng_deg, lat_deg) in degrees for an icon and a zoom

    Since we are using a World Mercator projection deformation is uniform in
    all directions and depends only on latitude
    """
    C = (2 * 6378137.0 * math.pi) / 256.  # one pixel
    C2 = (2 * 6378137.0 * math.pi) / 360.  # one degree

    lat_deformation = (C * math.cos(math.radians(lat)) / 2 ** zoom)

    lat_deg = (lat_deformation * pix_y) / C2
    lng_deg = (lat_deformation * pix_x) / C2

    return (lng_deg, lat_deg)


def update_minbbox(point, minbbox):
    """
    For every cluster we are calculating minimum bbox for Localities in the
    cluster

    This is required in order to have nicer click to zoom map behaviour
    (fitBounds)
    """

    new_minbbox = list(minbbox)

    if point[0] < minbbox[0]:
        new_minbbox[0] = point[0]
    if point[0] > minbbox[2]:
        new_minbbox[2] = point[0]
    if point[1] < minbbox[1]:
        new_minbbox[1] = point[1]
    if point[1] > minbbox[3]:
        new_minbbox[3] = point[1]

    return new_minbbox
