import base
from os import getenv
import django_heroku

base.SECRET_KEY = getenv('SECRET_KEY')

base.DEBUG = False

base.MEDIA_ROOT = base.BASE_DIR / 'uploads'

base.MEDIA_URL = '/uploaded-images/'

STATIC_ROOT = base.BASE_DIR / 'staticfiles'

django_heroku.settings(locals())
