import os
from .base import *
import cloudinary
from dotenv import load_dotenv


local_env_file = os.path.join(BASE_DIR, ".env")
if os.path.isfile(local_env_file):
    load_dotenv(local_env_file)
    
SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DJANGO_DEBUG', '') != 'False'

MEDIA_URL = '/uploaded-images/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage' 

STATIC_ROOT = BASE_DIR / 'staticfiles'


cloudinary.config(
    cloud_name = os.getenv('CLOUD_NAME'),
    api_key = os.getenv('CLOUD_API_KEY'),
    api_secret = os.getenv('CLOUD_API_SECRET')
)