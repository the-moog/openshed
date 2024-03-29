"""
Django settings for openshed project.

Generated by 'django-admin startproject' using Django 2.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from pathlib import Path
import hashlib
import logging

logger = logging.getLogger(__name__)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = Path(__file__).parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = hashlib.md5(Path("secretpass").open().read().strip().encode('utf-8'))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '*']



# Application definition

INSTALLED_APPS = [
    'openshed',
    'members.apps.MembersConfig',
    'items.apps.ItemsConfig',
    'lending.apps.LendingConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'widget_tweaks',
    'utilities',
    'address',
    'phone_field',
    'cart',
    'openshed.jsignature',
]

CART_SESSION_ID = 'cart'

# Allow passing of the CSRF token in the request header
CSRF_HEADER_NAME = 'X-CSRFToken'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'openshed.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['openshed/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                #'cart.context_processor.cart_total_amount'
            ],
        },
    },
]

WSGI_APPLICATION = 'openshed.wsgi.application'

# Login/Logout
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'equipment',
        'USER': 'equipment',
        'PASSWORD': Path("secretpass").open().read().strip(),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': 'openshed-dev.sqlite3',
#        'USER': '',
#        'PASSWORD': '',
#        'HOST': '',
#        'PORT': '',
#    },
#}

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = []

x = [{'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
     {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
     {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
     {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'}]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True
USE_TZ = False  # Store datetimes in UTC

# JSignature - We will provide our own button to match form style
# <input type='button' value='{{ reset_btn_text }}' class="btn">
#JSIGNATURE_RESET_BUTTON = False
JSIGNATURE_BUTTON_CSS_CLASS = 'btn btn-lg btn-dark'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / '../static'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / '../media'

print(f"MEDIA_ROOT : {MEDIA_ROOT}")
print(f"STATIC_ROOT: {STATIC_ROOT}")

#Django 3.2 Migration
#see https://dev.to/rubyflewtoo/upgrading-to-django-3-2-and-fixing-defaultautofield-warnings-518n
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

AUTH_USER_MODEL = "members.Member"

GOOGLE_API_KEY = 'AIzaSyD3xLJkVWir3ZzTjI_WPJygD3ilQoDAZA4'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'django.core': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
            'propagate': False,
        },
        'items': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
            #'filters': ['special']
        }
    },
}