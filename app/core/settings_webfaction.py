from .settings import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [
    'django-skeleton.bekonline.webfactional.com',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': '',
        'PORT': '',
        'NAME': 'django_skeleton',
        'USER': 'django_skeleton',
        'PASSWORD': 'yepR7fRuXebAdRaphurU2uB6StuSWa2r',
    }
}

STATIC_ROOT = '/home/bekonline/webapps/django_skeleton_static/static/'
STATIC_URL = 'http://django-skeleton.bekonline.webfactional.com/static/static/'

MEDIA_ROOT = '/home/bekonline/webapps/django_skeleton_static/media/'
MEDIA_URL = 'http://django-skeleton.bekonline.webfactional.com/static/media/'

