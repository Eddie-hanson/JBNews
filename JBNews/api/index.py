# api/index.py
import os
from JBNews.wsgi import application

# Ensure the production settings are used
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "JBNews.production_settings")

app = application
