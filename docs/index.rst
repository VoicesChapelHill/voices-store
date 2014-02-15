.. Voices Store documentation master file, created by
   sphinx-quickstart on Sun Feb  2 11:07:26 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Voices Store's documentation!
========================================

Contents:

.. toctree::
   :maxdepth: 2

   user
   staff

Running locally
---------------

Make virtualenv with Python 3.3, e.g. ``mkvirtualenv -p /usr/bin/python3.3 voices_store``
``pip install -r requirements/dev.txt``
Set SITE_ID=1 in environment
``cp voices_store/settings/local.py-example voices_store/settings/local.py``
edit local.py
python manage.py runserver


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

