"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import logging
import os

print("os.environ['DATABASE_URL']=%r" % os.environ.get('DATABASE_URL', None))

logger = logging.getLogger(__name__)

logger.info("In voices_store/wsgi.py")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'voices_store.settings.base')

from django.core.wsgi import get_wsgi_application
from dj_static import Cling  # , MediaCling
#application = Cling(MediaCling(get_wsgi_application()))
application = Cling(get_wsgi_application())
