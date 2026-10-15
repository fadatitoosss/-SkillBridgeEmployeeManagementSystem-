from .base import *
import os
DEBUG = False
SECRET_KEY = os.environ['DJANGO_SECRET_KEY']
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
# Trust Render's proxy HTTPS header (fixes redirect loops)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# Do NOT force HTTPS redirect — Render's proxy handles it
SECURE_SSL_REDIRECT = False
# Secure cookies
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# HSTS
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# Static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'