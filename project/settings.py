"""
Django settings for project project.
Optimized for both local development and Render.com deployment
"""

from pathlib import Path
import os
import sys
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security settings
SECRET_KEY = config('SECRET_KEY', default='django-insecure-development-key-change-in-production')

# IMPORTANT: Check if running on Render or locally
IS_RENDER = os.environ.get('RENDER', False)
IS_PRODUCTION = config('PRODUCTION', default=False, cast=bool)

# Set DEBUG based on environment
DEBUG = not IS_RENDER  # True locally, False on Render
if os.environ.get('DEBUG', '').lower() in ['true', '1', 't']:
    DEBUG = True

print(f"DEBUG: {DEBUG}")
print(f"IS_RENDER: {IS_RENDER}")
print(f"IS_PRODUCTION: {IS_PRODUCTION}")

# FIX: Improved ALLOWED_HOSTS configuration
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
    '.onrender.com',
    'lfcteensbyazhin.onrender.com',
]

# Get Render external hostname if available
RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# FIX: CSRF trusted origins - only HTTPS in production
CSRF_TRUSTED_ORIGINS = []
if IS_RENDER or IS_PRODUCTION:
    CSRF_TRUSTED_ORIGINS = [
        'https://localhost:8000',
        'https://lfcteensbyazhin.onrender.com',
        'https://*.onrender.com',
    ]
else:
    # Local development - allow HTTP
    CSRF_TRUSTED_ORIGINS = [
        'http://localhost:8000',
        'http://127.0.0.1:8000',
        'http://0.0.0.0:8000',
    ]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',  # For SEO
    
    # Cloudinary apps (optional)
    'cloudinary_storage',
    'cloudinary',
    
    # Your app
    'app',
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

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # Custom context processor for SEO
                'app.context_processors.seo_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database configuration - Using SQLite locally
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'  # Changed to Nigeria timezone
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files configuration
MEDIA_URL = '/media/'

# Cloudinary configuration - optional for local development
try:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default=''),
        'API_KEY': config('CLOUDINARY_API_KEY', default=''),
        'API_SECRET': config('CLOUDINARY_API_SECRET', default=''),
    }
    
    # Only use Cloudinary if credentials are provided
    if (CLOUDINARY_STORAGE['CLOUD_NAME'] and 
        CLOUDINARY_STORAGE['API_KEY'] and 
        CLOUDINARY_STORAGE['API_SECRET']):
        DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
        
        # Configure Cloudinary
        cloudinary.config(
            cloud_name=CLOUDINARY_STORAGE['CLOUD_NAME'],
            api_key=CLOUDINARY_STORAGE['API_KEY'],
            api_secret=CLOUDINARY_STORAGE['API_SECRET'],
            secure=True
        )
        print("Cloudinary storage enabled")
    else:
        DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
        print("Using local file storage (Cloudinary credentials not found)")
        
except ImportError:
    print("Cloudinary not installed. Using local file storage.")
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# WhiteNoise configuration for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# FIX: Security settings - Only enforce HTTPS in production
if IS_RENDER or IS_PRODUCTION:
    # Production settings - Force HTTPS
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    print("PRODUCTION MODE: HTTPS and security headers enforced")
else:
    # Development settings - Allow HTTP
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    X_FRAME_OPTIONS = 'SAMEORIGIN'
    print("DEVELOPMENT MODE: HTTP allowed")

# SEO Settings
SITE_NAME = "LFC Teens Byazhin"
SITE_DESCRIPTION = "A community of teenagers growing in faith, hope, and love through Jesus Christ. Join LFC Teens Byazhin for worship, fellowship, and spiritual growth."
SITE_KEYWORDS = "LFC Teens, Byazhin, Christian teens, youth ministry, Abuja church, Winners Chapel, teenage fellowship, spiritual growth"

# Add localhost to CSRF for development
if DEBUG:
    CSRF_TRUSTED_ORIGINS.append('http://localhost:8000')
    CSRF_TRUSTED_ORIGINS.append('http://127.0.0.1:8000')