from .base import *

import dj_database_url
import logging

print("This is settings.dokku")

DATABASES = {'default': dj_database_url.config()}
STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
STRIPE_PUBLISHABLE_KEY = os.environ['STRIPE_PUBLISHABLE_KEY']
MEMBER_PASSWORD = os.environ['MEMBER_PASSWORD']

# Log everything to stdout
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        },
    },

    'loggers': {
        '': {
            'level': logging.WARN,
            'handlers': ['console'],
        },
        'django': {
            'level': logging.WARN,
            'handlers': ['console'],
        },
    }
}

print("DATABASES=%r" % DATABASES)
