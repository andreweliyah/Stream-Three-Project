from base import *
import dj_database_url
 
DEBUG = False
 
DATABASES = {
    'default': dj_database_url.config('CLEARDB_DATABASE_URL')
}
 
# Stripe environment variables
STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE', '<your STRIPE_PUBLISHABLE key>')
STRIPE_SECRET = os.getenv('STRIPE_SECRET', '<your STRIPE SECRET key>')
 
SITE_URL = 'https://blogreaderpro.herokuapp.com/'
ALLOWED_HOSTS.append('blogreaderpro.herokuapp.com')
ALLOWED_HOSTS.append('herokuapp.com')
 
# Log DEBUG information to the console
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'DEBUG'),
        },
    },
}

SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')