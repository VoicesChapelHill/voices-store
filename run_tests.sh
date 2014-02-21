#!/bin/sh

flake8 accounting staff store users voices_store
coverage run manage.py test
