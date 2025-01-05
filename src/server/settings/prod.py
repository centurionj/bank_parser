from .base import *  # noqa

# Debug
DEBUG = False

# Host
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split(', ')

# SWAGGER
SWAGGER_SETTINGS['SECURE_SCHEMA'] = 'https'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
