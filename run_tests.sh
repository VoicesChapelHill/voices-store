#!/bin/sh
set -e

flake8 staff store users voices_store
coverage run manage.py test "$@"
coverage report -m
