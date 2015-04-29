#!/usr/bin/env python
import sys
import socket

import os

if __name__ == "__main__":
    from django.core.management import execute_from_command_line

    if socket.gethostname() == "web381.webfaction.com":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings_webfaction")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    execute_from_command_line(sys.argv)

