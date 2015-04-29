"""
WSGI config for the project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/wsgi/
"""
import socket

import os

if socket.gethostname() == "web381.webfaction.com":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings_webfaction")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

