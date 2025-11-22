"""
Django settings for project project.
"""

from pathlib import Path
import os
import sys
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings
SECRET_KEY = config('SECRET_KEY', default='django-insecure-fallback-key-for-dev')

DEBUG = config('DEBUG', default=True, cast=bool)  # Set to True for development

ALLOWED_HOSTS = [
    'naija-mall.onrender.com',
    'localhost',
    '127.0.0.1',
    '0.0.0.0',
]

CSRF_TRUSTED_ORIGINS = [
    'https://naija-mall.onrender.com',
    'https://*.onrender.com',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Cloudinary apps
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
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

# Database Configuration with Fallback
try:
    import dj_database_url
    DATABASE_URL = config('DATABASE_URL', default='')
    if DATABASE_URL:
        DATABASES = {
            'default': dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
    else:
        # Fallback to SQLite if no DATABASE_URL
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': BASE_DIR / 'db.sqlite3',
            }
        }
except ImportError:
    # Fallback if dj_database_url is not available
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
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'

# Cloudinary configuration
try:
    import cloudinary
    import cloudinary.uploader
    import cloudinary.api
    
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': config('CLOUDINARY_CLOUD_NAME', default='dkmk76rfw'),
        'API_KEY': config('CLOUDINARY_API_KEY', default='192649688938628'),
        'API_SECRET': config('CLOUDINARY_API_SECRET', default='7c92grhUwijRo5owpFKk7B62A_k'),
    }
    
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
    
    # Configure Cloudinary
    cloudinary.config(
        cloud_name=config('CLOUDINARY_CLOUD_NAME', default='dkmk76rfw'),
        api_key=config('CLOUDINARY_API_KEY', default='192649688938628'),
        api_secret=config('CLOUDINARY_API_SECRET', default='7c92grhUwijRo5owpFKk7B62A_k'),
        secure=True
    )
    
except ImportError:
    print("Cloudinary not installed. Using local file storage.")
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'