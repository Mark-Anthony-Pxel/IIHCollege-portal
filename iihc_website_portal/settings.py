from pathlib import Path
from django.contrib.messages import constants as message_constants
import dj_database_url
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-oa$q=rp#()uold@!7jjw*1@aa$(qx3!a1gn3p+38!3cvc!m586'

DEBUG = True  # Set this to False in production

ALLOWED_HOSTS = [
    'iih-college-portal.onrender.com',  
    'localhost',                         
    '127.0.0.1',                          
]


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')  
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')  
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_HOST_USER') 

# Configure message tags
MESSAGE_TAGS = {
    message_constants.INFO: "",
    message_constants.SUCCESS: "alert alert-success",
    message_constants.WARNING: "alert alert-warning",
    message_constants.ERROR: "alert alert-danger",
}

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'website_portal.backends.EmailBackend',
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

ASGI_APPLICATION = 'iihc_website_portal.asgi.application'

WSGI_APPLICATION = 'iihc_website_portal.wsgi.application'


DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://pixel:VfJKqUY65kF9UkFrCXpTFi9sGevAmPdL@dpg-csteerl6l47c73ek31p0-a.singapore-postgres.render.com/portal_uxnh',
        conn_max_age=600
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if not DEBUG:
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DATE_INPUT_FORMATS = [
    '%m/%d/%y', '%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%m-%d-%Y',
]
