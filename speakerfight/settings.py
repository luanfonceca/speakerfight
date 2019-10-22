#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Django settings for speakerfight project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
'''

from django.conf import global_settings
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hchgjid4s$nhe_@3*ildx480lpld*t$cs*#qvg((j_+g4zr++8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Template
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # hardcoded for override the external app's template
            os.path.join(BASE_DIR, *'speakerfight core templates'.split()),
        ],
        'OPTIONS': {
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
            'debug': DEBUG,
            # See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
            # https://docs.djangoproject.com/en/dev/ref/templates/api/#loader-types
            'loaders': [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    },
]

# Absolute path to the directory static files should be collected to.
STATICFILES_DIRS = []

STATIC_ROOT = os.path.join(BASE_DIR, "static")
DEFAULT_FROM_EMAIL = NO_REPLY_EMAIL = 'Speakerfight <noreply@speakerfight.com>'

ALLOWED_HOSTS = [
    "localhost",
    "127.0.0.1",
    "speakerfight.com",
]

# Media files.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Application definition
DEFAULT_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'activelink',
    'django_extensions',
    'vanilla',
    'bootstrap3',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.facebook',
    'debug_toolbar',
    'datetimewidget',
    'raven.contrib.django.raven_compat',
    'rest_framework',
    'anymail',
    'fixmydjango',
]

LOCAL_APPS = [
    'deck',
    'core',
    'jury',
    'api',
    'organization',
]

INSTALLED_APPS = LOCAL_APPS + THIRD_PARTY_APPS + DEFAULT_APPS

ROOT_URLCONF = 'speakerfight.urls'

WSGI_APPLICATION = 'speakerfight.wsgi.application'

EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3'
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

TIME_ZONE = 'America/Sao_Paulo'

LANGUAGE_CODE = 'en-US'

LANGUAGES = (
    ('en-us', _('English')),
    ('pt-br', _('Portuguese')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, "locale"),
)

# TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATETIME_INPUT_FORMATS = [
    '%d/%m/%Y %H:%M',
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

SITE_ID = 1

AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS + [
    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

MIDDLEWARE_CLASSES = global_settings.MIDDLEWARE_CLASSES + [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'locale_middleware.LocaleMiddleware',
]

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/userinfo.email'
        ],
        'AUTH_PARAMS': {'access_type': 'online'}
    },
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'METHOD': 'oauth2',
        'LOCALE_FUNC': lambda request: 'pt_BR',
        'VERIFIED_EMAIL': False
    }
}

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/events/'
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_REQUIRED = True
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_SIGNUP_FORM_CLASS = 'core.forms.SignupForm'

# Django Debug Toolbar
DEBUG_TOOLBAR_PATCH_SETTINGS = False

# Smart urls
SURL_REGEXERS = {
    'username': '[\w@.-]+'
}

SEND_NOTIFICATIONS = True

try:
    from local_settings import *
except ImportError:
    pass
