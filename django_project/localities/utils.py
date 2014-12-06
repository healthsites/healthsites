# -*- coding: utf-8 -*-
from django.template import Template, Context
from django.contrib.gis.geos import Polygon


def render_fragment(template, context):
    """
    Render a template fragment using provided context
    """

    t = Template(template)
    c = Context(context)
    return t.render(c)


def parse_bbox(bbox):
    """
    Convert a textual bbox to a GEOS polygon object

    This function assumes that any raised exceptions will be handled upstream
    """

    tmp_bbox = [float(coord) for coord in bbox.split(',')]

    if tmp_bbox[0] > tmp_bbox[2] or tmp_bbox[1] > tmp_bbox[3]:
            # bbox is not properly formatted minLng, minLat, maxLng, maxLat
            raise ValueError
    # create polygon from bbox
    return Polygon.from_bbox(tmp_bbox)
