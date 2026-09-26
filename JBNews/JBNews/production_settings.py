# JBNews/settings/prod.py
import os
import dj_database_url
from decouple import config
from .base_settings import *

DEBUG = False
PROD_DOMAIN = config("PROD_DOMAIN", default="")

ALLOWED_HOSTS = [".vercel.app"]
if PROD_DOMAIN:
    ALLOWED_HOSTS += [PROD_DOMAIN, f"www.{PROD_DOMAIN}"]
if os.environ.get("VERCEL_URL"):
    ALLOWED_HOSTS.append(os.environ["VERCEL_URL"])

CSRF_TRUSTED_ORIGINS = ["https://*.vercel.app"]
if PROD_DOMAIN:
    CSRF_TRUSTED_ORIGINS += [
        f"https://{PROD_DOMAIN}",
        f"https://www.{PROD_DOMAIN}",
    ]

SITE_URL = f"https://{config('PROD_DOMAIN', default='')}"

DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=0,  # Important for serverless!
        ssl_require=True
    )
}

# Set a shorter connection timeout for serverless environments
DATABASES['default']['OPTIONS'] = {
    'connect_timeout': 5,
}

# Media — Vercel has no persistent disk so use Cloudinary
STORAGES = {
    "default": {
        "BACKEND": "cloudinary_storage.storage.MediaCloudinaryStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
CLOUDINARY_STORAGE = {
    "CLOUD_NAME": config("CLOUDINARY_CLOUD_NAME"),
    "API_KEY":    config("CLOUDINARY_API_KEY"),
    "API_SECRET": config("CLOUDINARY_API_SECRET"),
}

# --- Proxy / TLS ---
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 3600           # raise once verified
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False

# Security headers
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"
