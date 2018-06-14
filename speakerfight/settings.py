#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
Django settings for speakerfight project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
'''

import os

import decouple

import dj_database_url

from django.conf import global_settings
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'hchgjid4s$nhe_@3*ildx480lpld*t$cs*#qvg((j_+g4zr++8'
SECRET_KEY = decouple.config('SECRET_KEY', cast=str, default='secret')

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = decouple.config('DEBUG', cast=bool, default=False)

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
# STATICFILES_DIRS = [
#     os.path.join(PROJECT_ROOT, 'static'),
# ]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
DEFAULT_FROM_EMAIL = NO_REPLY_EMAIL = 'Speakerfight <noreply@speakerfight.com>'

ALLOWED_HOSTS = [
    '*',
]

# Media files.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

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

EMAIL_BACKEND = decouple.config(
    'EMAIL_BACKEND', cast=str,
    default='django.core.mail.backends.locmem.EmailBackend'
)

if EMAIL_BACKEND.endswith('mailgun.EmailBackend'):
    MAILGUN_API_KEY = decouple.config('MAILGUN_API_KEY', cast=str)

# Database

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///{path}/db.sqlite3'.format(path=BASE_DIR),
        conn_max_age=500
    )
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

TIME_ZONE = 'America/Sao_Paulo'

LANGUAGE_CODE = decouple.config('LANGUAGE_CODE', cast=str, default='en-US')

LANGUAGES = (
    ('en-us', _('English')),
    ('pt-br', _('Portuguese')),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
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

# Django extension
EXTENSIONS_MAX_UNIQUE_QUERY_ATTEMPTS = 1000

# Sentry
RAVEN_CONFIG = {
    'dsn': decouple.config('RAVEN_CONFIG_DSN', cast=str, default=''),
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'DEBUG',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'DEBUG',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}
