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
DEV_TRACKER_PLAN = '<PLAN>'
 
# Paypal environment variables
SITE_URL = 'http://127.0.0.1:8000'
PAYPAL_NOTIFY_URL = '<your ngrok URL>'
PAYPAL_RECEIVER_EMAIL = '<your Paypal merchant email>'

SECURE_SSL_REDIRECT = False
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')