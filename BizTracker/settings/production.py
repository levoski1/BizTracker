# settings/production.py
from .base import *

DEBUG = False

ALLOWED_HOSTS = ['yourdomain.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'yourdbname',
        'USER': 'yourdbuser',
        'PASSWORD': 'yourdbpassword',
        'HOST': 'yourdbhost',
        'PORT': 'yourdbport',
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
