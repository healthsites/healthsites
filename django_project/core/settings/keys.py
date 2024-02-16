# coding=utf-8
"""
core.settings.contrib
"""
import os

CAPTCHA_SITE_KEY = os.environ.get('CAPTCHA_SITE_KEY', '')
CAPTCHA_SECRET_KEY = os.environ.get('CAPTCHA_SECRET_KEY', '')
SOCIAL_AUTH_OPENSTREETMAP_KEY = os.environ.get('SOCIAL_AUTH_OPENSTREETMAP_KEY', '')
SOCIAL_AUTH_OPENSTREETMAP_SECRET = os.environ.get('SOCIAL_AUTH_OPENSTREETMAP_SECRET', '')