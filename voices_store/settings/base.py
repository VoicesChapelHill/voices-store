"""
Django settings for voices_store project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7q=f3$l#8(0v!mqc9%n3r7uzkww)*9n_hq*d_%@4pz^v^7(egl'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 3rd party:
    'south',
    'django_browserid',  # Load after auth
    'bootstrap3',
    # This project:
    'accounting',
    'store',
    'staff',
    'users',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
)

ROOT_URLCONF = 'voices_store.urls'

WSGI_APPLICATION = 'voices_store.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
# This is from me:
APP_DIR = os.path.dirname(BASE_DIR)  # APP_DIR is the dir containing manage.py etc.
# So put static_root parallel to our other top-level dirs
STATIC_ROOT = os.path.join(APP_DIR, 'static_root')

# Default - put them in our own dir (will override in dokku settings as it won't work there)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(APP_DIR, 'media_root')


# Add the django_browserid authentication backend.
AUTHENTICATION_BACKENDS = (
   'django.contrib.auth.backends.ModelBackend', # required for admin
   'django_browserid.auth.BrowserIDBackend',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.request',
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'django_browserid.context_processors.browserid',
)

# Set your site url for security
BROWSERID_AUDIENCES = [
    'http://0.0.0.0:8000',
    'https://store.voiceschapelhill.org',
]
BROWSERID_CREATE_USER = 'users.utils.create_user'

LOGIN_REDIRECT_URL = reverse_lazy('logged_in')


AUTH_USER_MODEL = 'users.VoicesUser'
