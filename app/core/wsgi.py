"""
WSGI config for django-skeleton project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import socket

if socket.gethostname() == "web381.webfaction.com":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings_webfaction")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

