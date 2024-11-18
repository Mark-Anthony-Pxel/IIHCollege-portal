from pathlib import Path
import dj_database_url
from django.contrib.messages import constants as message_constants
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-n&q%g+ju@we4a=v2+(cyl^%gc4m^x+(yg%c1c&_l&+qg1!p921'

ALLOWED_HOSTS = [
    'https://iih-college-portal.onrender.com',  
    'localhost',                         
    '127.0.0.1',                          
]

# Configure message tags
MESSAGE_TAGS = {
    message_constants.INFO: "",
    message_constants.SUCCESS: "alert alert-success",
    message_constants.WARNING: "alert alert-warning",
    message_constants.ERROR: "alert alert-danger",
}

# backend-email
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'website_portal.backends.EmailBackend',
    # 'website_portal.backends.TeacherBackend',
]


# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'daphne',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website_portal',
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

ROOT_URLCONF = 'iihc_website_portal.urls'

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

WSGI_APPLICATION = 'iihc_website_portal.wsgi.application'

ASGI_APPLICATION = "iihc_website_portal.asgi.application"

# Security settings
# SECURE_SSL_REDIRECT = True  # Redirect all HTTP requests to HTTPS
# SECURE_HSTS_SECONDS = 3600  # Enable HTTP Strict Transport Security (HSTS)
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': dj_database_url.config(
        # Replace this value with your local database's connection string.
        default='postgresql://pxel:yYWsgntkKJ4v0qykPoGMMksGxYSplWtE@dpg-cspd4jbtq21c739ro8n0-a.oregon-postgres.render.com/',
        # iihcdatabase
        conn_max_age=600
    )
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

# Build paths inside the project like this: BASE_DIR / 'subdir'.

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# This is where static files will be collected
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Using the '/' operator to join paths

STATICFILES_DIRS = [
    BASE_DIR / 'static',  # Adjust this path as needed
]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Check if in DEBUG mode
DEBUG = False  # Set this to False in production

if not DEBUG:
    # Enable the WhiteNoise storage backend for serving static files in production
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.redis.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',  # Redis server location
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     },
#     'secondary': {
#         'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
#         'LOCATION': '/var/tmp/django_cache',  # Path for file-based cache
#     }
# }

DATE_INPUT_FORMATS = [
    '%m/%d/%y',   # MM/DD/YY
    '%Y-%m-%d',   # YYYY-MM-DD
    '%d/%m/%Y',   # DD/MM/YYYY
    '%d-%m-%Y',   # DD-MM-YYYY
    '%m-%d-%Y',   # MM-DD-YYYY
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media' 