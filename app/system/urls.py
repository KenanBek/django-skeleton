from django.conf.urls import patterns, url, include

info_urlpatterns = patterns('system.info',
    url(r'^request/$', 'request_info', name='system_info_request'),
)

urlpatterns = patterns('system.views',
    # info jsons
    url(r'^info/', include(info_urlpatterns)),
    # pages
    url(r'^localization/$', 'localization', name='system_localization'),
    # requests
    #url(r'^language/(?P<lang>[\w-]+)/$', 'language', name='system_language'),
)

