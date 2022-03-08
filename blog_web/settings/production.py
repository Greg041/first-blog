from .base import *
from os import getenv

SECRET_KEY = getenv('SECRET_KEY')

DEBUG = False

MEDIA_ROOT = BASE_DIR / 'uploads'

MEDIA_URL = '/uploaded-images/'

STATIC_ROOT = BASE_DIR / 'staticfiles'

