"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""
import logging
import os

logger = logging.getLogger(__name__)

logger.info("In voices_store/wsgi.py")


from voices_store.guess_settings import guess_settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", guess_settings())

from django.core.wsgi import get_wsgi_application
from dj_static import Cling
application = Cling(get_wsgi_application())
