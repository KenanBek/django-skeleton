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
    url(r'^confirm/(?P<activation_key>\w+)/', 'register_confirm', name='account_register_confirm'),
    url(r'^change/(?P<activation_key>\w+)/', 'email_change_confirm', name='account_email_change_confirm'),
    url(r'^restore_password/$', 'restore_password', name='account_restore_password'),
    url(r'^reset_password/(?P<activation_key>\w+)/', 'reset_password', name='account_reset_password'),
)

