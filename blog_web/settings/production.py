from .base import *
import django_heroku

DEBUG = False

MEDIA_ROOT = BASE_DIR / 'uploads'

MEDIA_URL = '/uploaded-images/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

django_heroku.settings(locals())
