import os
from .base import *
import cloudinary

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = False

MEDIA_URL = '/uploaded-images/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage' 

STATIC_ROOT = BASE_DIR / 'staticfiles'

cloudinary.config(
    cloud_name = os.getenv('CLOUD_NAME'),
    api_key = os.getenv('CLOUD_API_KEY'),
    api_secret = os.getenv('CLOUD_API_SECRET')
)