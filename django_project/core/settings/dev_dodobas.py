# -*- coding: utf-8 -*-
from os.path import abspath, dirname, join, pardir

from .dev import *  # noqa

PROJECT_PATH = abspath(join(dirname(__file__), pardir, pardir))
MEDIA_ROOT = join(PROJECT_PATH, 'media')
STATIC_ROOT = join(PROJECT_PATH, 'static')

