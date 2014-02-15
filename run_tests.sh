#!/bin/sh

flake8 accounting staff store users voices_store
python manage.py test
