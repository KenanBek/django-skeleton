from django.conf import settings
from ipware.ip import get_real_ip, get_ip

from . import abstracts
from . import models


class EventLogger(object):
    def __init__(self, title, user=None):
        self.title = title
        self.user = user
        event = models.Event()
        event.title = self.title
        event.user = self.user
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


class CoreLogic(abstracts.LogicAbstract):
    request = None
    user = None

    def __init__(self, request):
        super(CoreLogic, self).__init__(request)
        if not request.user.is_anonymous():
            self.user = request.user

        self.settings_manager = SettingsManager()

    def new_event_logger(self, title):
        event_logger = EventLogger(title, self.user)
        return event_logger

    def store_request(self):
        if not settings.APPLICATION_MONITORING:
            return
        if not settings.APPLICATION_MONITOR_STUFF_USERS and self.request.user.is_staff:
            return
        user_request = models.Request()

        user_request.server_name = self.request.META.get('SERVER_NAME', '')
        user_request.server_host = self.request.META.get('HTTP_HOST', '')

        user_request.user_username = self.request.user.username
        user_request.user_is_staff = self.request.user.is_staff
        user_request.user_is_active = self.request.user.is_active

        user_request.client_name = self.request.META.get('USER', '')
        user_request.client_agent = self.request.META.get('HTTP_USER_AGENT', '')

        user_request.client_ip = self.request.META.get('REMOTE_ADDR', '')
        real_ip = get_real_ip(self.request)
        if real_ip is None:
            real_ip = get_ip(self.request)
        user_request.client_real_ip = real_ip

        user_request.scheme = self.request.scheme
        user_request.method = self.request.method
        user_request.data = self.request.REQUEST

        user_request.is_ajax = self.request.is_ajax()

        user_request.from_page = self.request.META.get('HTTP_REFERER', '')
        user_request.to_page = self.request.path
        user_request.to_page_query = self.request.META.get('QUERY_STRING', '')

        user_request.save()
        return user_request

