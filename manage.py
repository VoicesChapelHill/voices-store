#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    from voices_store.guess_settings import guess_settings
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", guess_settings())

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
