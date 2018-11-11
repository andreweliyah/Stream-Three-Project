from base import *
import dj_database_url
 
DEBUG = False
 
DATABASES = {
    'default': dj_database_url.config('CLEARDB_DATABASE_URL')
}
 
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