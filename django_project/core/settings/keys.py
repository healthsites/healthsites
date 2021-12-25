# coding=utf-8
"""
core.settings.contrib
"""
import os

CHAPCHA_SITE_KEY = os.environ.get('CHAPCHA_SITE_KEY', '')
CHAPCHA_SECRET_KEY = os.environ.get('CHAPCHA_SECRET_KEY', '')
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', '')
SOCIAL_AUTH_OPENSTREETMAP_KEY = os.environ.get('SOCIAL_AUTH_OPENSTREETMAP_KEY', '')
SOCIAL_AUTH_OPENSTREETMAP_SECRET = os.environ.get('SOCIAL_AUTH_OPENSTREETMAP_SECRET', '')
