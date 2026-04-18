from myinventory.settings import *
import os

# Security
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static files
STATIC_ROOT = '/app/staticfiles'
STATIC_URL = '/static/'

MEDIA_ROOT = '/app/media'
MEDIA_URL = '/media/'

# Database (optional PostgreSQL)
if os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(default=os.environ.get('DATABASE_URL'))
from myinventory.settings import *
import os

# Security
DEBUG = False
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')
SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True') == 'True'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Static files
STATIC_ROOT = '/app/staticfiles'
STATIC_URL = '/static/'

MEDIA_ROOT = '/app/media'
MEDIA_URL = '/media/'

# Database (optional PostgreSQL)
if os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES['default'] = dj_database_url.config(default=os.environ.get('DATABASE_URL'))
