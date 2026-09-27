# JBNews/base_settingsbase.py

from pathlib import Path
import os
from decouple import config, AutoConfig


BASE_DIR = Path(__file__).resolve().parent.parent
config = AutoConfig(search_path=BASE_DIR)

SECRET_KEY = config("SECRET_KEY")

INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'NewsApp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'JBNews.urls'
WSGI_APPLICATION = 'JBNews.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'NewsApp.context_processors.base_context',
            ],
        },
    },
]

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Accra'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = f'JBNews Ghana <{EMAIL_HOST_USER}>'

# Jazzmin
JAZZMIN_SETTINGS = {
    'site_title':         'JB News Admin',
    'site_header':        'JBNews Admin Dashboard',
    'site_brand':         'Admin Dashboard',
    'site_logo':          'img/Jbnew_logo (1).jpeg',
    'login_logo':         'img/Jbnew_logo (1).jpeg',
    'site_logo_classes':  'img-fluid',
    'login_logo_classes': 'img-fluid',
    'site_icon':          'img/Jbnew_logo (1).jpeg',
    'custom_css':         'css/admin_custom.css',
    'welcome_sign':       'Welcome to JBNews Admin',
    'copyright':          'JBNews',
    'topmenu_links':      [{'app': 'NewsApp'}],
}

JAZZMIN_UI_TWEAKS = {
    'theme':           'simplex',
    'dark_mode_theme': 'darkly',
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
