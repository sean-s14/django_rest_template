"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', None)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False if os.environ.get('DJANGO_DEBUG', None) == 'False' else True

ENV_DOMAIN = os.environ.get('ENV_DOMAIN', None)
ADMIN_PATH = os.environ.get('ADMIN_PATH', None)
HOST_IP = os.environ.get('HOST_IP', None)

ALLOWED_HOSTS = ['localhost', HOST_IP, ENV_DOMAIN]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # 3rd Party
    'rest_framework',
    'corsheaders',

    # Custom
    'auth2',
]

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 3rd Party
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",  # 3rd Party
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME':     os.environ.get('DB_NAME', None),
        'USER':     os.environ.get('DB_USER', None),
        'PASSWORD': os.environ.get('DB_PASSWORD', None),
        'HOST':     os.environ.get('DB_HOST', None),
        'PORT':     os.environ.get('DB_PORT', None),
    }
}


import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env) if os.environ.get('DJANGO_DEV', False) == False else None


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_DIRS = [ os.path.join(BASE_DIR, 'static') ]
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'auth2.User'

AUTHENTICATION_BACKENDS = [
    'auth2.backend.ModelBackend',
    # 'django.contrib.auth.backends.ModelBackend',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.AllowAny'
        'rest_framework.permissions.IsAuthenticated'  # TODO: Add this when ready
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # New
        # 'custom_auth.models.CustomTokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ]
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # 'ACCESS_TOKEN_LIFETIME': timedelta(seconds=3),  # For Testing
    # 'REFRESH_TOKEN_LIFETIME': timedelta(seconds=6),
    "ROTATE_REFRESH_TOKENS": True,
    "UPDATE_LAST_LOGIN": True,
}


# Sendgrid
# EMAIL_BACKEND = "sgbackend.SendGridBackend"
# SENDGRID_API_KEY = os.environ["SENDGRID_API_KEY"]
# SENDGRID_SANDBOX_MODE_IN_DEBUG = os.environ['SENDGRID_SANDBOX_MODE_IN_DEBUG']
# SENDGRID_ECHO_TO_STDOUT = os.environ['SENDGRID_ECHO_TO_STDOUT']
# DEFAULT_FROM_EMAIL = os.environ['DJANGO_DEFAULT_FROM_EMAIL']
# CONTACT_EMAIL = os.environ['DJANGO_CONTACT_EMAIL']


# Stripe
# STRIPE_PK_KEY = os.environ['STRIPE_PK_KEY']  # Public Key (development)
# STRIPE_SK_KEY = os.environ['STRIPE_SK_KEY']  # Secret Key (development)
# STRIPE_WEBHOOK_SK = os.environ['STRIPE_WEBHOOK_SK']

# APPEND_SLASH = False

CORS_ALLOWED_ORIGINS = []
 
CORS_ALLOWED_ORIGINS_DEV = os.environ.get("CORS_ALLOWED_ORIGINS_DEV", None)
if CORS_ALLOWED_ORIGINS_DEV is not None:
    CORS_ALLOWED_ORIGINS.append(CORS_ALLOWED_ORIGINS_DEV)

CORS_ALLOWED_ORIGINS_PROD = os.environ.get("CORS_ALLOWED_ORIGINS_PROD", None)
if CORS_ALLOWED_ORIGINS_PROD is not None:
    CORS_ALLOWED_ORIGINS.append(CORS_ALLOWED_ORIGINS_PROD)

# CORS_ORIGIN_ALLOW_ALL = True