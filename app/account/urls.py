from django.conf.urls import patterns, url, include
from django.views.generic import RedirectView


ajax_urlpatterns = patterns('account.ajax',
    url(r'^login/$', 'login', name='account_ajax_login'),
)

urlpatterns = patterns('account.views',
    # General
    url(r'^$', RedirectView.as_view(url='/account/index', permanent=True)),
    url(r'^index/$', 'index', name='account_index'),
    url(r'^login/$', 'login', name='account_login'),
    url(r'^register/$', 'register', name='account_register'),
    url(r'^logout/$', 'logout', name='account_logout'),
    # AJAX
    url(r'^ajax/', include(ajax_urlpatterns)),
)

