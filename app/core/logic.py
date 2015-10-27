from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import LANGUAGE_SESSION_KEY, check_for_language
from ipware.ip import get_real_ip, get_ip
from django.db.models import Q

from . import models
from blog import models as blog_models

''' Entities '''


class Client(object):
    local_ip = None
    global_ip = None
    user = None  # Instance of django.contrib.auth.models.User
    language = None  # Language code
    language_obj = None  # Instance of core.models.Language


''' Utils '''


class EventLogger(object):
    title = None
    client = None
    event = None

    def __init__(self, title, client):
        self.title = title
        self.client = client
        event = models.Event()
        event.title = self.title
        event.user = self.client.user
        event.client_local_ip = self.client.local_ip
        event.client_global_ip = self.client.global_ip
        event.save()
        self.event = event

    def new_log(self, level, text, *args):
        log = models.Log()
        log.event = self.event
        log.level = level
        log.text = text.format(*args)
        log.save()

    def new_debug_log(self, text, *args):
        self.new_log(models.LOG_LEVEL_DEBUG, text, *args)

    def new_info_log(self, text, *args):
        self.new_log(models.LOG_LEVEL_INFO, text, *args)

    def new_warning_log(self, text, *args):
        self.new_log(models.LOG_LEVEL_WARNING, text, *args)

    def new_error_log(self, text, *args):
        self.new_log(models.LOG_LEVEL_ERROR, text, *args)

    def new_critical_log(self, text, *args):
        self.new_log(models.LOG_LEVEL_CRITICAL, text, *args)


''' Managers '''


class SettingsManager(object):
    def __init__(self):
        self.queryset = models.Settings.objects

    def get(self, key):
        try:
            return self.queryset.get(key=key)
        except models.Settings.MultipleObjectsReturned:
            return self.queryset.filter(key=key).all()
        except models.Settings.DoesNotExist:
            return None

    def get_by_group(self, key, group):
        try:
            return self.queryset.get(key=key, group=group)
        except models.Settings.DoesNotExist:
            return None

    def get_all(self):
        return self.queryset.all()

    def get_dict(self):
        result = {}

        un_grouped_settings = self.queryset.filter(group__exact='')
        for item in un_grouped_settings:
            result[item.key] = item.value

        grouped_settings = self.queryset.exclude(group__isnull=True).exclude(group__exact='')
        if grouped_settings.count():
            grouped_settings = list(grouped_settings)
            groups_dict = {}
            for item in grouped_settings:
                group_values = groups_dict.get(item.group, {})
                group_values[item.key] = item.value
                groups_dict[item.group] = group_values
            result['groups'] = groups_dict

        return result


class BrowserStoreManager(object):
    DEFAULT_MAX_AGE = 604800
    DEFAULT_EXPIRES = None
    DEFAULT_PATH = '/'
    DEFAULT_DOMAIN = None
    DEFAULT_SECURE = False
    DEFAULT_HTTPONLY = False

    def __init__(self, request):
        self.request = request

    def get_session_value(self, key):
        return self.request.session.get(key)

    def get_cookie_value(self, key):
        return self.request.COOKIES.get(key)

    def get(self, key):
        if hasattr(self.request, 'session'):
            return self.get_session_value(key)
        else:
            return self.request.COOKIES.get(key)

    def set_session_value(self, key, value):
        self.request.session[key] = value
        self.request.session.save()

    def set_cookie_value(self, key, value, response):
        response.set_cookie(key, value,
            max_age=self.DEFAULT_MAX_AGE,
            path=self.DEFAULT_PATH,
            domain=self.DEFAULT_DOMAIN)

    def set(self, key, value, response=None):
        if hasattr(self.request, 'session'):
            self.set_session_value(key, value)
        else:
            if response:
                self.set_cookie_value(key, value, response)


''' Elements '''


class DataController(object):
    client = None

    def __init__(self, client):
        self.client = client

    @staticmethod
    def get_languages():
        return models.Language.objects.filter(is_active=True).all()

    @staticmethod
    def get_language(code):
        return models.Language.objects.get(code=code)

    @staticmethod
    def check_for_language(code):
        return models.Language.objects.filter(code=code).exists()


class ViewPage(object):
    SESSION_APP_LANGUAGE_KEY = 'app_lang'
    DEFAULT_LANGUAGE_CODE = 'en'

    request = None
    client = None
    context = None
    settings_manager = None
    browser_store_manager = None

    def __init__(self, request):
        self.request = request
        # Initialize managers
        self.settings_manager = SettingsManager()
        self.browser_store_manager = BrowserStoreManager(self.request)
        # Set initial values
        self._set_client()
        self._set_context()

    ''' Private members '''

    def _check_for_language(self, code):
        return DataController.check_for_language(code)

    def _set_client(self):
        self.client = Client()
        # Set local ip
        self.client.local_ip = self.request.META.get('REMOTE_ADDR', '')
        # Set global ip
        self.client.global_ip = get_real_ip(self.request)
        if self.client.global_ip is None:
            self.client.global_ip = get_ip(self.request)
        # Set user instance
        self.client.user = self.request.user
        # Set language
        current_language_code = self.browser_store_manager.get(self.SESSION_APP_LANGUAGE_KEY)
        if not current_language_code:
            current_language_code = self.DEFAULT_LANGUAGE_CODE
        try:
            self.set_language(current_language_code)
        except:
            self.set_language(self.DEFAULT_LANGUAGE_CODE)

    def _set_context(self):
        self.context = {
            'client': self.client,
            'languages': DataController.get_languages()
        }

    ''' Public members '''

    def is_get(self):
        return self.request.method == "GET"

    def is_post(self):
        return self.request.method == "POST"

    def is_ajax(self):
        return self.request.is_ajax()

    def store_request(self):
        if not settings.APPLICATION_MONITORING:
            return
        if not settings.APPLICATION_MONITOR_STUFF_USERS and self.request.user.is_staff:
            return
        user_request = models.Request()

        user_request.server_name = self.request.META.get('SERVER_NAME', '')
        user_request.server_host = self.request.META.get('HTTP_HOST', '')

        user_request.user_username = self.client.user.username
        user_request.user_is_staff = self.client.user.is_staff
        user_request.user_is_active = self.client.user.is_active

        user_request.client_name = self.request.META.get('USER', '')
        user_request.client_agent = self.request.META.get('HTTP_USER_AGENT', '')

        user_request.client_local_ip = self.client.local_ip
        user_request.client_global_ip = self.client.global_ip

        user_request.scheme = self.request.scheme
        user_request.method = self.request.method
        user_request.data = self.request.REQUEST

        user_request.is_ajax = self.request.is_ajax()

        user_request.from_page = self.request.META.get('HTTP_REFERER', '')
        user_request.to_page = self.request.path
        user_request.to_page_query = self.request.META.get('QUERY_STRING', '')

        user_request.save()
        return user_request

    def set_to_context(self, key, value):
        self.context[key] = value

    def set_language(self, code, response=None):
        if not (self._check_for_language(code) and check_for_language(code)):
            raise Exception(_("Given language code ({}) is not correct!".format(code)))
        self.browser_store_manager.set(self.SESSION_APP_LANGUAGE_KEY, code, response=response)
        self.browser_store_manager.set(LANGUAGE_SESSION_KEY, code, response=response)
        self.client.language = code
        self.client.language_obj = DataController.get_language(code)

    def get_param(self, key):
        if self.request.method == 'GET':
            return self.request.GET.get(key, None)
        else:
            return self.request.POST.get(key, None)

    def get_params(self, key):
        if self.request.method == 'GET':
            return self.request.GET.getlist(key, None)
        else:
            return self.request.POST.getlist(key, None)

    def new_event_logger(self, title):
        event_logger = EventLogger(title, self.client)
        return event_logger

    def search(self, term):
        pages = blog_models.Page.objects.filter(Q(title__contains=term) | Q(content__contains=term))
        posts = blog_models.Post.objects.filter((Q(title__contains=term)
                                                 | Q(short_content__contains=term)
                                                 | Q(full_content__contains=term))
                                                & Q(status=blog_models.ITEM_STATUS_PUBLISHED))

        result = {}
        result['pages'] = pages
        result['posts'] = posts

        return result


from django.http import HttpResponse
import json


def search_autocomplete(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        posts = blog_models.Post.objects.filter(Q(title__contains=q))
        results = []

        for post in posts:
            autocomplete_json = {}
            autocomplete_json['id'] = post.id
            autocomplete_json['label'] = post.title
            autocomplete_json['desc'] = 'Post'
            autocomplete_json['value'] = post.title
            autocomplete_json['url'] = reverse('blog_post', kwargs={'post_id': post.pk, 'post_slug': post.slug})
            results.append(autocomplete_json)
        pages = blog_models.Page.objects.filter(Q(title__contains=q))
        for page in pages:
            autocomplete_json = {}
            autocomplete_json['id'] = page.id
            autocomplete_json['label'] = post.title
            autocomplete_json['desc'] = 'Page'
            autocomplete_json['value'] = page.title
            autocomplete_json['value'] = page.title
            results.append(autocomplete_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)