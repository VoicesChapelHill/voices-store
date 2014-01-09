import socket

def guess_settings():
    # Return name of a settings module to use given the current environment
    hostname = socket.getfqdn()
    if hostname.startswith("dokku"):
        return "voices_store.settings.dokku"
    return "voices_store.settings.local"
