import logging
import os
import pwd


logger = logging.getLogger(__name__)


def dumpenv():
    keys = sorted(os.environ.keys())
    for k in keys:
        print("%s=%s" % (k, os.environ[k]))


def guess_settings():

    #dumpenv()

    #logname = pwd.getpwuid(os.getuid())[0]
    #print("logname=%s" % logname)

    # Return name of a settings module to use given the current environment
    if os.path.exists('.heroku'):
        return "voices_store.settings.dokku"
    return "voices_store.settings.local"
