from os import getenv
from .base import *
import django_heroku
import cloudinary
import cloudinary_storage

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

STATIC_ROOT = BASE_DIR / 'staticfiles'

django_heroku.settings(locals())

MEDIA_ROOT = BASE_DIR / 'uploads'

MEDIA_URL = '/uploaded-images/'

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUD_NAME'),
    'API_KEY': os.getenv('API_KEY'),
    'API_SECRET': os.getenv('API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage' 

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')