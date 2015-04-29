from django.contrib import admin

from . import models

''' Event '''


class EventAdminAbstract(models.ModelAdminAbstract):
    list_filter = ['added_at', 'uuid', 'title', 'identifier']
    list_display = ['added_at', 'uuid', 'title', 'identifier', 'logs', ]

    def logs(self, obj):
        return obj.log_set.count()


class LogAdminAbstract(models.ModelAdminAbstract):
    list_filter = ['added_at', 'level', ]
    list_display = ['added_at', 'event', 'level', 'text', ]


admin.site.register(models.Event, EventAdminAbstract)
admin.site.register(models.Log, LogAdminAbstract)

''' Request '''


class RequestAdmin(models.ModelAdminAbstract):
    list_filter = ('user_username', 'user_is_staff', 'user_is_active', 'client_real_ip',
                   'scheme', 'method', 'is_ajax', )
    list_display = ('added_at', 'user_username', 'user_is_staff', 'user_is_active',
                    'client_name', 'client_ip', 'client_real_ip', 'client_agent',
                    'server_name', 'server_host',
                    'scheme', 'method',
                    'from_page', 'to_page', 'to_page_query',
                    'is_ajax',)


admin.site.register(models.Request, RequestAdmin)
