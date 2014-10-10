"""
Django settings for django-skeleton project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Base configuration

SECRET_KEY = '=37nsotr=ct-bc5gwbbvo^@s3*w=hib%i^plnbzn8758n$4pz='
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'suit',
    'reversion',
    'ckeditor',
    'django_select2',
    'import_export',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'system',
    'account',
    'website',
)
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'files/documents/development.sqlite3'),
    }
}

# Internationalization and Localization

LANGUAGE_CODE = 'en'
USE_TZ = True
USE_I18N = True
USE_L10N = True
DATE_FORMAT = 'd/m/Y'
DATETIME_FORMAT = 'd/m/Y P'
SHORT_DATE_FORMAT = 'd/m/Y'
SHORT_DATETIME_FORMAT = 'd/m/Y P'
DATETIME_INPUT_FORMAT = (
    '%Y-%m-%d %H:%M:%S',  # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',  # '2006-10-25 14:30'
    '%Y-%m-%d',  # '2006-10-25'
    '%d/%m/%Y %H:%M:%S',  # '25/10/2006 14:30:59'
    '%d/%m/%Y %H:%M:%S.%f',  # '25/10/2006 14:30:59.000200'
    '%d/%m/%Y %H:%M',  # '25/10/2006 14:30'
    '%d/%m/%Y',  # '25/10/2006'
    '%d/%m/%y %H:%M:%S',  # '25/10/06 14:30:59'
    '%d/%m/%y %H:%M:%S.%f',  # '25/10/06 14:30:59.000200'
    '%d/%m/%y %H:%M',  # '25/10/06 14:30'
    '%d/%m/%y',  # '25/10/06'
)

# Templates

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
)
TEMPLATE_CONTEXT_PROCESSORS = TCP + (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages'
)
TEMPLATE_DIRS = {
    os.path.join(BASE_DIR, 'files/templates/'),
}


# Static files (CSS, JavaScript, Images)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'files/static'),
)
STATIC_URL = '/static/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'files/publish')

# Media files (user uploaded)

MEDIA_ROOT = os.path.join(BASE_DIR, 'files/media')
MEDIA_URL = '/media/'

# Fixtures

FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'files/fixtures/'),
)

# Logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s %(name)s-%(levelname)s (%(filename)s:%(lineno)s %(funcName)s)]: %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '[%(asctime)s %(name)s-%(levelname)s]: %(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'file-django': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'files/logs/django.log'),
            'formatter': 'verbose'
        },
        'file-application': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'files/logs/application.log'),
            'formatter': 'verbose'
        },
        'file-logic': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'files/logs/logic.log'),
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file-django'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'application': {
            'handlers': ['file-application'],
            'propagate': True,
            'level': 'DEBUG',
        },
        'logic': {
            'handlers': ['file-logic'],
            'propagate': True,
            'level': 'DEBUG',
        },
    }
}

# Django Suit configuration example

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Administration',
    'HEADER_DATE_FORMAT': 'l, j. F Y',
    'HEADER_TIME_FORMAT': 'H:i',
    # forms
    # 'SHOW_REQUIRED_ASTERISK': True,  # Default True
    # 'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    # 'SEARCH_URL': '/admin/auth/user/',
    # 'MENU_ICONS': {
    # 'sites': 'icon-leaf',
    #    'auth': 'icon-lock',
    # },
    # 'MENU_OPEN_FIRST_CHILD': True, # Default True
    # 'MENU_EXCLUDE': ('auth.group',),
    # 'MENU': (
    #     'sites',
    #     {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
    #     {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
    #     {'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
    # ),

    # misc
    # 'LIST_PER_PAGE': 15
}

# CKEDITOR

CKEDITOR_UPLOAD_PATH = 'ckeditor/'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': '100%',
        'width': '100%',
    },
    'basic': {
        'toolbar': 'Basic',
        'height': '100%',
        'width': '100%',
    },
}

