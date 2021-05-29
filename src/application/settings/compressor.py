from .settings import *

STATICFILES_FINDERS += (
    'compressor.finders.CompressorFinder',
)
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter',  'compressor.filters.cssmin.CSSMinFilter']

COMPRESS_ENABLED = True
COMPRESS_OUTPUT_DIR = 'cached'
COMPRESS_ROOT = STATIC_ROOT
