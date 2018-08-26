from base import *
 
DEBUG = True
 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
 
# Stripe environment variables
STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE', '<ADD YOUR KEY>')
STRIPE_SECRET = os.getenv('STRIPE_SECRET', '<ADD YOUR KEY>')
DEV_TRACKER_PLAN = os.getenv('STRIPE_PLAN', '<your STRIPE PLAN key>')

SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')