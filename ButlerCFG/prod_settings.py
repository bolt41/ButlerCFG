import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hjhkjhkjh780908khv_d)u2sqtj95ci2!xjqtw4dtvfk4nc$gf+43my0+g'


DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', '192.168.1.32']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'butlerdb',
        'USER': 'butler',
        'PASSWORD': 'butler',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIR = [STATIC_DIR]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')