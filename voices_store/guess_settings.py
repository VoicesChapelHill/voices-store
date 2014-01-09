import logging
import socket

logger = logging.getLogger(__name__)


def guess_settings():
    # Return name of a settings module to use given the current environment
    hostname = socket.getfqdn()
    logger.info("hostname=%s" % hostname)
    if hostname.startswith("dokku"):
        return "voices_store.settings.dokku"
    return "voices_store.settings.local"
