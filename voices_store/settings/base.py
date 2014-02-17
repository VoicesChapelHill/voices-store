import os
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse_lazy

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!


DEBUG = False
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    # This project: (first so our templates etc override other modules')
    'accounting',
    'store',
    'staff',
    'users',
    # Django
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # The Django sites framework is required by django-allauth (bummer)
    'django.contrib.sites',
    # django-allauth:
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # ... include the providers you want to enable:
    #'allauth.socialaccount.providers.amazon',
    #'allauth.socialaccount.providers.facebook',
    #'allauth.socialaccount.providers.google',
    #'allauth.socialaccount.providers.linkedin',
    #'allauth.socialaccount.providers.persona',
    #'allauth.socialaccount.providers.twitter',
    # other 3rd party:
    'south',
    'bootstrap3',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
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

# Default - put them in our own dir (will override in heroku settings as it won't work there)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(APP_DIR, 'media_root')


TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    'django.core.context_processors.request',
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'store.utils.cart_template_context',
    # Required by allauth template tags
    "django.core.context_processors.request",
    # allauth specific context processors
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
)
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USER_DISPLAY = lambda user: user.get_full_name().strip() or user.email
ACCOUNT_USERNAME_BLACKLIST = ['admin', 'root', 'webmaster', 'postmaster']
ACCOUNT_USERNAME_REQUIRED = False

LOGIN_REDIRECT_URL = reverse_lazy('logged_in')  # if user hasn't given name, asks them for it

AUTH_USER_MODEL = 'users.VoicesUser'

# Load site defs
FIXTURE_DIRS = [
    os.path.join(BASE_DIR, "fixtures"),
]


SITE_ID = int(os.environ['SITE_ID'])

if SITE_ID == 1:
    # 0.0.0.0:8000

    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    TEMPLATE_STRING_IF_INVALID = "ERR[%s]"

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "voices_store",
            "USER": "",
            "PASSWORD": "",
            "HOST": "",
            "PORT": "",
            }
    }
    INSTALLED_APPS += ("debug_toolbar", )
    INTERNAL_IPS = ("127.0.0.1",)

    MIDDLEWARE_CLASSES += \
        ("debug_toolbar.middleware.DebugToolbarMiddleware", )

    SESSION_COOKIE_SECURE = False
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'unique-snowflake'
        }
    }

    ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Voices store (local dev)] '

    # Set these in local.py
    #STRIPE_SECRET_KEY = 'xxx'
    #STRIPE_PUBLISHABLE_KEY = 'xxx'
    #MEMBER_PASSWORD = 'xxx'
    #SECRET_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    LOGGING = {
        'version': 1,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler'
            },
        },
    }
    # Locally only, allow overriding
    local_settings = os.path.join(BASE_DIR, 'settings', 'local.py')
    if os.path.exists(local_settings):
        from .local import *  # noqa


elif SITE_ID == 2:
    # test.chapelhillcommunitychorus.org
    INTERNAL_IPS = ['24.225.71.109']
    ACCOUNT_EMAIL_SUBJECT_PREFIX = '[Voices store (test.chapelhillcommunitychorus.org)] '

    import dj_database_url

    DATABASES = {'default': dj_database_url.config()}
    STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']
    STRIPE_PUBLISHABLE_KEY = os.environ['STRIPE_PUBLISHABLE_KEY']
    MEMBER_PASSWORD = os.environ['MEMBER_PASSWORD']
    SECRET_KEY = os.environ['SECRET_KEY']
else:
    raise ImproperlyConfigured("Unknown SITE_ID %s set in environment" % SITE_ID)
