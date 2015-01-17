"""
Django settings for the project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import constants as message_constants

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Base configuration

SECRET_KEY = '=37nsotr=ct-bc5gwbbvo^@s3*w=hib%i^plnbzn8758n$4pz='
DEBUG = True
TEMPLATE_DEBUG = True
JSON_DEBUG = False
ALLOWED_HOSTS = [
    'localhost'
]

# Application definition

INSTALLED_APPS = (
    'suit',
    'rest_framework',
    'ckeditor',
    'django_select2',
    'easy_thumbnails',
    'debreach',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'system',
    'account',
    'website',
    'cart',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',  # must be at the start
    'htmlmin.middleware.HtmlMinifyMiddleware',  # must be at the start but after gzip middleware
    'debreach.middleware.RandomCommentMiddleware',  # must be at the start but after compression middleware
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # must be before common and after session middleware
    'django.middleware.common.CommonMiddleware',
    'debreach.middleware.CSRFCryptMiddleware',  # must be before default csrf middleware
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.ClientMiddleware',
)
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
ROOT_URLCONF = 'core.urls'
WSGI_APPLICATION = 'core.wsgi.application'

# Auth

AUTH_PROFILE_MODULE = 'account.Profile'
LOGIN_URL = '/account/login/'
LOGOUT_URL = '/account/logout/'
ANONYMOUS_USER_ID = -1

# Message

MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'danger'
}

# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'files/documents/development.sqlite3'),
    }
}

# Internationalization and Localization

LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('az', _('Azerbaijan')),
    ('ru', _('Russian')),
    ('en', _('English')),
)
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'files/locale/'),
)
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
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.i18n',
    'core.context.general',
    'debreach.context_processors.csrf',  # must be at the end
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

# Application Configuration

APPLICATION_URL = 'http://localhost:8000'
APPLICATION_CONFIG = {
    'title': 'Project Title',
    'description': _('Project Description.'),
    'copyright': '&copy; 2015 ProjectDomain.com',
    'author': 'ProjectDomain.com',
    'admin_title': 'Project Title',
    'page_default_author': 'ProjectDomain.com',
    'page_default_description': 'Project Description',
    'google_id': 'google-id',
    'facebook_id': '1520447268200947',
    'twitter_id': 'twitter-id',
    'date_format': 'dd/mm/yyyy'
}
APPLICATION_CONTENT_COUNT = 10
APPLICATION_CONTENT_MAXIMUM_COUNT = 20
APPLICATION_DUMMY_DATA_COUNT = 7
APPLICATION_FROM_EMAIL = 'Project Title <noreply@projectdomain.com>'
APPLICATION_EMAIL_MANUAL_TIMEOUT = 3  # In minutes
APPLICATION_SYSTEM_STORE_USER_REQUESTS = DEBUG

# DJANGO SUIT

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Administration',
    'HEADER_DATE_FORMAT': 'l, j. F Y',
    'HEADER_TIME_FORMAT': 'H:i',
    # forms
    # 'SHOW_REQUIRED_ASTERISK': True,  # Default True
    # 'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    'SEARCH_URL': '/search/',
    # 'MENU_ICONS': {
    # 'sites': 'icon-leaf',
    # 'auth': 'icon-lock',
    # },
    # 'MENU_OPEN_FIRST_CHILD': True, # Default True
    # 'MENU_EXCLUDE': ('auth.group',),
    # 'MENU': (
    # 'sites',
    # {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
    # {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
    # {'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
    # ),
    'MENU': (
        'sites',
        '-',
        {'label': 'Account', 'icon': 'icon-lock', 'models': (
            {'model': 'auth.group', 'label': 'Group'},
            {'model': 'auth.user', 'label': 'User'},
            {'model': 'account.profile', 'label': 'Profile'},
        )},
        '-',
        {'label': 'Website', 'icon': 'icon-th', 'models': (
            {'model': 'website.contact', 'label': 'Contacts'},
            {'model': 'website.subscriber', 'label': 'Subscribers'},
            {'model': 'website.document', 'label': 'Documents'},
            {'model': 'website.slider', 'label': 'Sliders'},
            {'model': 'website.slide', 'label': 'Slides'},
        )},
        {'label': 'Page', 'icon': 'icon-th', 'models': (
            {'model': 'website.widget', 'label': 'Widgets'},
            {'model': 'website.page', 'label': 'Pages'},
        )},
        {'label': 'Post', 'icon': 'icon-th', 'models': (
            {'model': 'website.category', 'label': 'Categories'},
            {'model': 'website.post', 'label': 'Posts'},
        )},
        '-',
        {'label': 'Cart', 'icon': 'icon-th', 'models': (
            {'model': 'cart.currency', 'label': 'Currencies'},
            {'model': 'cart.manufacturer', 'label': 'Manufactureres'},
            {'model': 'cart.category', 'label': 'Categories'},
            {'model': 'cart.attributegroup', 'label': 'Attribute groups'},
            {'model': 'cart.attribute', 'label': 'Attributes'},
        )},
        {'label': 'Shop', 'icon': 'icon-th', 'models': (
            {'model': 'cart.product', 'label': 'Products'},
            {'model': 'cart.shop', 'label': 'Shops'},
            {'model': 'cart.shopproduct', 'label': 'Shops and Products'},
        )},
        {'label': 'Orders', 'icon': 'icon-th', 'models': (
            {'model': 'cart.productreview', 'label': 'Product reviews'},
            {'model': 'cart.shopreview', 'label': 'Shop reviews'},
        )},
        '-',
        {'label': 'Documentation', 'icon': 'icon-bookmark', 'url': 'https://github.com/KenanBek/django-skeleton/wiki'},
        {'label': 'Report a bug', 'icon': 'icon-comment', 'url': 'http://github.com/kenanbek/django-skeleton/issues'},
    ),
    # misc
    'LIST_PER_PAGE': 50
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

# EASY-THUMBNAILS

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True},
        'small': {'size': (125, 125), 'crop': True},
        'medium': {'size': (400, 400), 'crop': True},
        'normal': {'size': (600, 600), 'crop': True},
        'large': {'size': (800, 800), 'crop': True},
    },
}

