# JBNews/settings/prod.py

from .base_settings import *

DEBUG = False

ALLOWED_HOSTS = [
    ".vercel.app",
    config("PROD_DOMAIN", default=""),
    f"www.{config('PROD_DOMAIN', default='')}",
]

CSRF_TRUSTED_ORIGINS = [
    f"https://{config('PROD_DOMAIN', default='')}",
    f"https://www.{config('PROD_DOMAIN', default='')}",
    "https://*.vercel.app",
]

SITE_URL = f"https://{config('PROD_DOMAIN', default='')}"

DATABASES = {
    "default": {
        "ENGINE":   "django.db.backends.postgresql",
        "NAME":     config("DB_NAME"),
        "USER":     config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST":     config("DB_HOST"),
        "PORT":     config("DB_PORT", default="5432"),
    }
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

# Security headers
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
X_FRAME_OPTIONS = "DENY"
