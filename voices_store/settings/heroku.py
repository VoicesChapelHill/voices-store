from .base import *  # noqa

import os
import dj_database_url

DATABASES = {'default': dj_database_url.config()}

STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
STRIPE_PUBLISHABLE_KEY = os.environ['STRIPE_PUBLISHABLE_KEY']
MEMBER_PASSWORD = os.environ['MEMBER_PASSWORD']
SECRET_KEY = os.environ['SECRET_KEY']
