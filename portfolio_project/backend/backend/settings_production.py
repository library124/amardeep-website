"""
Production settings for Django deployment on Render.com
Following SOLID principles for secure and scalable deployment
"""

import os
import dj_database_url
from .settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Production hosts
ALLOWED_HOSTS = [
    '.onrender.com',
    'amardeep-portfolio-backend.onrender.com',
    'localhost',
    '127.0.0.1',
]

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    "https://amardeep-portfolio-frontend.vercel.app",
    "https://amardeepasode.com",
    "https://www.amardeepasode.com",
    "http://localhost:3000",  # For development
]

CORS_ALLOW_CREDENTIALS = True

# Database configuration for production
if 'DATABASE_URL' in os.environ:
    DATABASES['default'] = dj_database_url.parse(os.environ['DATABASE_URL'])
    DATABASES['default']['CONN_MAX_AGE'] = 600

# Static files configuration for production with WhiteNoise
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# WhiteNoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Add WhiteNoise to middleware
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Media files configuration
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings for production
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Use environment variables for sensitive data
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)

# Email configuration for production
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', EMAIL_HOST_USER)
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', EMAIL_HOST_PASSWORD)
BREVO_API_KEY = os.environ.get('BREVO_API_KEY', BREVO_API_KEY)

# Razorpay configuration for production
RAZORPAY_KEY_ID = os.environ.get('RAZORPAY_KEY_ID', RAZORPAY_KEY_ID)
RAZORPAY_KEY_SECRET = os.environ.get('RAZORPAY_KEY_SECRET', RAZORPAY_KEY_SECRET)
RAZORPAY_WEBHOOK_SECRET = os.environ.get('RAZORPAY_WEBHOOK_SECRET', RAZORPAY_WEBHOOK_SECRET)

# Frontend URL for production
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'https://amardeep-portfolio-frontend.vercel.app')

# Logging configuration for production
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'portfolio_app': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Cache configuration for production
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# Session configuration
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True

# Additional security headers
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True