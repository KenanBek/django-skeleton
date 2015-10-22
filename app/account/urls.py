from django.conf.urls import patterns, url
from django.views.generic import RedirectView

urlpatterns = patterns('account.views',
    # General
    url(r'^$', RedirectView.as_view(url='/account/index', permanent=True)),
    url(r'^index/$', 'index', name='account_index'),
    url(r'^login/$', 'login', name='account_login'),
    url(r'^register/$', 'register', name='account_register'),
    url(r'^logout/$', 'logout', name='account_logout'),
    url(r'^modify/$', 'modify_account', name='account_modify'),
    url(r'^change_password/$', 'change_password', name='account_change_password'),
    url(r'^restore_password/$', 'restore_password', name='account_restore_password'),
    url(r'^request_confirm/(?P<activation_key>\w+)/', 'request_confirm', name='account_request_confirm'),
    url(r'^change_email/$', 'change_email', name='account_change_email'),
)