"""
Django settings for the project.
"""
import logging
import os

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages import constants as message_constants

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # use os.path.join(BASE_DIR, ...)

# Base configuration

SECRET_KEY = '=37nsotr=ct-bc5gwbbvo^@s3*w=hib%i^plnbzn8758n$4pz='
SITE_ID = 1
DEBUG = True
TEMPLATE_DEBUG = DEBUG
JSON_DEBUG = False
ALLOWED_HOSTS = [
    'localhost'
]

# Logging configuration

DJANGO_LOGGER = logging.getLogger('django')
APPLICATION_LOGGER = logging.getLogger('application')
CORE_LOGGER = logging.getLogger('core')

# Email configuration

EMAIL_HOST = 'host'
EMAIL_HOST_USER = 'user'
EMAIL_HOST_PASSWORD = 'password'
ADMINS = (
    ('Kenan Bek', 'mail@kenanbek.me'),
)
MANAGERS = ADMINS

# Application definition

INSTALLED_APPS = (
    'suit',
    'rest_framework',
    'ckeditor',
    'django_select2',
    'easy_thumbnails',
    'debreach',
    'compressor',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'debug_toolbar',
    'template_timings_panel',
    'core',
    'account',
    'blog',
    'cart',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',  # must be at the start
    'debreach.middleware.RandomCommentMiddleware',  # must be at the start but after compression middleware
    # Minify and Cache
    'django.middleware.cache.UpdateCacheMiddleware',  # as high (top) as possible
    'htmlmin.middleware.HtmlMinifyMiddleware',  # must be after UpdateCacheMiddleware
    #
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # must be after encode middlewares
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # must be before common and after session middleware
    'django.middleware.common.CommonMiddleware',
    'debreach.middleware.CSRFCryptMiddleware',  # must be before default csrf middleware
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.CoreMiddleware',
    # Fetch page cache and mark for minifier
    'django.middleware.cache.FetchFromCacheMiddleware',  # must be at the end
    'htmlmin.middleware.MarkRequestMiddleware',  # must be after FetchFromCacheMiddleware
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
TIME_ZONE = 'Asia/Baku'
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
    # Others
    'compressor.finders.CompressorFinder',
)
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'files/public/static')

# Media files (user uploaded)

MEDIA_ROOT = os.path.join(BASE_DIR, 'files/public/media')
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
    'title': _('Project Title'),
    'short_title': _('PT'),
    'author': 'Kenan Bek, http://kenanbek.me',
    'slogan': _('Code while alive!'),
    'description': _('Project Description.'),
    'keywords': _('django, project, template, skeleton, base'),
    'copyright': "&copy; 2015 <a href='http://example.com'>Example Co.</a>",
    'google_id': 'google-id',
    'facebook_id': '1520447268200947',
    'twitter_id': 'twitter-id',
    'date_format': 'dd/mm/yyyy'
}
APPLICATION_CONTENT_COUNT = 10
APPLICATION_CONTENT_MAXIMUM_COUNT = 20
APPLICATION_DUMMY_DATA_COUNT = 7
APPLICATION_FROM_EMAIL = 'Title <noreply@projectdomain.com>'
APPLICATION_EMAIL_MANUAL_TIMEOUT = 3  # In minutes
APPLICATION_MONITORING = DEBUG
APPLICATION_MONITOR_STUFF_USERS = DEBUG

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
    'MENU': (
        'sites',
        # Core
        '-',
        {'label': 'Core', 'icon': 'icon-th', 'models': (
            {'model': 'core.settings', 'label': 'Settings'},
            {'model': 'core.event', 'label': 'Events'},
            {'model': 'core.log', 'label': 'Logs'},
            {'model': 'core.request', 'label': 'Requests'},
        )},
        # Account
        '-',
        {'label': 'Account', 'icon': 'icon-lock', 'models': (
            {'model': 'auth.group', 'label': 'Group'},
            {'model': 'auth.user', 'label': 'User'},
            {'model': 'account.profile', 'label': 'Profile'},
        )},
        # Blog
        '-',
        {'label': 'Blog', 'icon': 'icon-th', 'models': (
            {'model': 'blog.contact', 'label': 'Contacts'},
            {'model': 'blog.subscriber', 'label': 'Subscribers'},
            {'model': 'blog.document', 'label': 'Documents'},
            {'model': 'blog.slider', 'label': 'Sliders'},
            {'model': 'blog.slide', 'label': 'Slides'},
        )},
        {'label': 'Page', 'icon': 'icon-th', 'models': (
            {'model': 'blog.widget', 'label': 'Widgets'},
            {'model': 'blog.page', 'label': 'Pages'},
        )},
        {'label': 'Post', 'icon': 'icon-th', 'models': (
            {'model': 'blog.category', 'label': 'Categories'},
            {'model': 'blog.post', 'label': 'Posts'},
        )},
        # Cart
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
        # Others
        '-',
        {'label': 'Documentation', 'icon': 'icon-bookmark', 'url': 'https://github.com/KenanBek/django-skeleton/wiki'},
        {'label': 'Report a bug', 'icon': 'icon-comment', 'url': 'http://github.com/kenanbek/django-skeleton/issues'},
    ),
    # misc
    'LIST_PER_PAGE': 50
}

# CKEDITOR

CKEDITOR_UPLOAD_PATH = 'plugin/ckeditor/'
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

# EASY THUMBNAILS

THUMBNAIL_ALIASES = {
    '': {
        'avatar': {'size': (50, 50), 'crop': True},
        'small': {'size': (125, 125), 'crop': True},
        'medium': {'size': (400, 400), 'crop': True},
        'normal': {'size': (600, 600), 'crop': True},
        'large': {'size': (800, 600), 'crop': True},
        'xxl': {'size': (1024, 728), 'crop': True},
    },
}
THUMBNAIL_NAMER = 'easy_thumbnails.namers.source_hashed'

# DEBUG TOOLBAR

DEBUG_TOOLBAR_PATCH_SETTINGS = DEBUG
DEBUG_TOOLBAR_PANELS = (
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
    'template_timings_panel.panels.TemplateTimings.TemplateTimings',
)

# HTML MIN

HTML_MINIFY = True  # not DEBUG
EXCLUDE_FROM_MINIFYING = ('^admin/', )
KEEP_COMMENTS_ON_MINIFYING = False

