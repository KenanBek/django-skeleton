#!/usr/bin/env python
import os
import sys
import socket

from core import configuration as core_configuration

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    core_configuration.configure()

    if socket.gethostname() == "web381.webfaction.com":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings_webfaction")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    execute_from_command_line(sys.argv)

