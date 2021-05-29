# Django settings for project.
# These settings are common settings for ALL possible environments: development, production, testing, etc.
# To set the custom settings for a particular environment use its own settings file (e.g. production.py)

# Import other settings
from .admin_tools import *
from .filebrowser import *
from .ckeditor import *
from .statistics import *
from .email import *
from .celery import *
from .shop import *
from .sms import *

# Imports and directories
import os
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), os.pardir))

# System settings
FORCE_SCRIPT_NAME = ''
SECRET_KEY = 'g#%u0r4he3rrc6p844plgr$nmx89qdkdnvq6^ryblp9n7xshyz'
ROOT_URLCONF = 'application.urls'
WSGI_APPLICATION = 'application.wsgi.application'
AUTH_USER_MODEL = 'shop.User'

# Administration
ADMINS = (
    ('Developer', 'mail@engine2.ru'),
)
MANAGERS = ADMINS

# Debug and run options
DEBUG = False
HTML_MINIFY = True
ALLOWED_HOSTS = ['*']

# Database
DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'www_mandarin_one',
        'USER':     'postgres',
        'PASSWORD': 'postgres',
        'HOST':     'localhost',
        'PORT':     '',
    }
}

# Applications
INSTALLED_APPS = (

    # Third django packages
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'ckeditor',
    'compressor',
    'filebrowser',
    'mptt',
    'sorl.thumbnail',


    # Developer django packages
    'ajax',
    'cache_model',
    'mail',
    'pages',
    'preferences',
    'public_model',
    'seo',
    'sort_model',

    # Developer django admin packages
    'server_resources',    

    # Standard django packages
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'django.contrib.postgres',

    # Application packages
    'application.website',
    'application.shop',

)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'pages.middleware.PageMiddleware',
)

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.contrib.messages.context_processors.messages',
                'django.contrib.auth.context_processors.auth',
                'preferences.context_processors.preferences',
                'pages.context_processors.page',
                'pages.context_processors.history',
            ],
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
                'admin_tools.template_loaders.Loader',
            ],
            'debug': DEBUG,
        },
    },
]

# Internationalization
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = False
LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

# Media and static files
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Cache
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/0",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        'TIMEOUT': 6000
    }
}
