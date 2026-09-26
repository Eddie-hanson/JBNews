"""
ASGI config for JBNews project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

settings_module = (
    "JBNews.productions_settings"
    if os.environ.get("VERCEL") == "true"
    else "JBNews.settings"
)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    settings_module
)

application = get_asgi_application()
app = application
