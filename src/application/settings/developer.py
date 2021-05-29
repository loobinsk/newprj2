from .settings import *

DEBUG = True
HTML_MINIFY = False
COMPRESS_ENABLED = False

INSTALLED_APPS += (
    'debug_toolbar',
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
) + MIDDLEWARE_CLASSES

INTERNAL_IPS = ('127.0.0.1', )

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
