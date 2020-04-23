"""
WSGI config for opsu project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

# Standard Libraries
import os
import sys

# Django Libraries
from django.core.wsgi import get_wsgi_application

sys.path.append("~/opsu")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "opsu.settings")

application = get_wsgi_application()
