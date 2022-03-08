from os import getenv
from .base import *
import django_heroku

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

MEDIA_ROOT = BASE_DIR / 'uploads'

MEDIA_URL = '/uploaded-images/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

django_heroku.settings(locals())
