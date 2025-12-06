"""
Django settings for project project.
Optimized for both local development and Render.com deployment
"""

from pathlib import Path
import os
import sys

# Try to import decouple.config, but fall back to os.environ if python-decouple isn't installed.
try:
    from decouple import config
except Exception:
    # minimal drop-in replacement for the few uses below
    def config(key, default=None, cast=None):
        val = os.environ.get(key, default)
        if cast and callable(cast):
            try:
                return cast(val)
            except Exception:
                return default
        return val

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Ensure MEDIA_ROOT always defined (prevents UnboundLocalError later)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings
SECRET_KEY = config('SECRET_KEY', default='django-insecure-development-key-change-in-production')

# IMPORTANT: Check if running on Render or locally
# Normalize environment flags to booleans robustly
RENDER_ENV = os.environ.get('RENDER', '')
IS_RENDER = str(RENDER_ENV).lower() in ['1', 'true', 't', 'yes']

IS_PRODUCTION = config('PRODUCTION', default=False, cast=bool)

# Set DEBUG based on environment (explicit DEBUG env var overrides)
DEBUG = not IS_RENDER
env_debug = os.environ.get('DEBUG', '')
if str(env_debug).lower() in ['true', '1', 't', 'yes']:
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

# CSRF trusted origins: use HTTPS in production; allow HTTP locally.
CSRF_TRUSTED_ORIGINS = []
if IS_RENDER or IS_PRODUCTION:
    # In production we expect HTTPS origins. Keep these explicit.
    CSRF_TRUSTED_ORIGINS = [
        'https://lfcteensbyazhin.onrender.com',
    ]
else:
    # Local development - allow HTTP on common dev ports.
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

# Optionally include WhiteNoise middleware only if available
_middleware = [
    'django.middleware.security.SecurityMiddleware',
]
try:
    import whitenoise  # type: ignore
    _middleware.append('whitenoise.middleware.WhiteNoiseMiddleware')
    whitenoise_available = True
except Exception:
    whitenoise_available = False

_middleware += [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

MIDDLEWARE = _middleware

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
TIME_ZONE = 'Africa/Lagos'
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
    import cloudinary  # type: ignore
    import cloudinary.uploader  # type: ignore
    import cloudinary.api  # type: ignore

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

except Exception:
    print("Cloudinary not installed or not configured. Using local file storage.")
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# WhiteNoise configuration for static files (only set if whitenoise is available)
if whitenoise_available:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
else:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

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

# Add localhost to CSRF for development (dedupe)
if DEBUG:
    for origin in ('http://localhost:8000', 'http://127.0.0.1:8000'):
        if origin not in CSRF_TRUSTED_ORIGINS:
            CSRF_TRUSTED_ORIGINS.append(origin)
