from django.conf import settings
from ipware.ip import get_real_ip, get_ip

from . import models

''' Entities '''


class Client(object):
    local_ip = None
    global_ip = None
    user = None  # Instance of django.contrib.auth.models.User
    language = None  # Language code
    language_obj = None  # Instance of news.models.Language


''' Abc '''


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


class SettingsManager(object):
    def __init__(self):
        self.queryset = models.Settings.objects
        pass

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


''' Base logical elements '''


class PageLogic(object):
    SESSION_LANGUAGE_KEY = 'app_lang'

    request = None
    client = None
    context = None
    settings_manager = None

    def __init__(self, request):
        self.request = request
        self._set_client()
        self._set_context()
        self._store_request()
        self.settings_manager = SettingsManager()

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
        self.client.language = self.request.session.get(self.SESSION_LANGUAGE_KEY, None)
        if not self.client.language:
            app_lang = 'en'
            self.request.session[self.SESSION_LANGUAGE_KEY] = app_lang
            self.request.session.save()
            self.client.language = app_lang
        pass
        # self.client.language_obj = NewsController.get_language(self.client.language)

    def _set_context(self):
        self.context = {
            'client': self.client,
        }

    def _store_request(self):
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

    def set_language(self, code):
        self.request.session[self.SESSION_LANGUAGE_KEY] = code
        self.request.session.save()

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

