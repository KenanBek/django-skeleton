from django.conf.urls import patterns, url

urlpatterns = patterns('system.views',
    url(r'^requestinfo/$', 'request_info', name='system_requestinfo'),
)

