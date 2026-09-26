# """
# WSGI config for JBNews project.

# It exposes the WSGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
# """

# import os

# from django.core.wsgi import get_wsgi_application
# if os.environ.get("VERCEL"):
#     os.environ.setdefault(
#         "DJANGO_SETTINGS_MODULE",
#         "JBNews.production_settings"
#     )
# else:
#     os.environ.setdefault(
#         "DJANGO_SETTINGS_MODULE",
#         "JBNews.settings"
#     )

# # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'JBNews.settings')

# application = get_wsgi_application()
# app = application

"""
WSGI config for JBNews project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "JBNews.production_settings"
)

application = get_wsgi_application()
app = application
