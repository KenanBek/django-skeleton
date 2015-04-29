from django.contrib import admin

from . import models
from . import abstracts

''' Settings '''


class SettingsAdmin(abstracts.ModelAdminAbstract):
    list_filter = ['group', ]
    list_display = ['key', 'value', 'group', ]


admin.site.register(models.Settings, SettingsAdmin)

''' Event '''


class EventAdmin(abstracts.ModelReadOnlyAdminAbstract):
    search_fields = ['title', 'user', ]
    list_filter = ['added_at']
    list_display = ['added_at', 'title', 'user', 'logs', ]

    def logs(self, obj):
        return obj.log_set.count()


class LogAdmin(abstracts.ModelReadOnlyAdminAbstract):
    list_filter = ['added_at', 'level', ]
    list_display = ['added_at', 'event', 'level', 'text', ]


admin.site.register(models.Event, EventAdmin)
admin.site.register(models.Log, LogAdmin)

''' Request '''


class RequestAdmin(abstracts.ModelReadOnlyAdminAbstract):
    search_fields = ['user_username', 'client_real_ip', 'from_page', 'to_page', 'to_page_query', ]
    list_filter = ['added_at', 'user_is_staff', 'user_is_active', 'scheme', 'method', 'is_ajax', ]
    list_display = ['added_at', 'user_username', 'client_real_ip',
                    'user_is_staff', 'user_is_active',
                    'scheme', 'method',
                    'from_page', 'to_page', 'to_page_query',
                    'is_ajax', ]


admin.site.register(models.Request, RequestAdmin)

