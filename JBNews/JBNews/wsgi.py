"""
WSGI config for JBNews project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
settings_module = (
    "JBNews.productions_settings"
    if os.environ.get("VERCEL") == "true"
    else "JBNews.settings"
)

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    settings_module
)

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JBNews.settings')

application = get_wsgi_application()
app = application
