# Local imports
from .base import *
# Third party imports
import cloudinary
import dj_database_url
from dotenv import load_dotenv
import os


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

ALLOWED_HOSTS = ['web-production-7672.up.railway.app/', '127.0.0.1']

CSRF_TRUSTED_ORIGINS = ['https://web-production-7672.up.railway.app/']

# Database connection
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.config(
        conn_max_age=500,
        conn_health_checks=True,
    )