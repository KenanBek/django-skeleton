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
    url(r'^confirm/(?P<activation_key>\w+)/', 'register_confirm', name='account_modify'),
    url(r'^change/(?P<activation_key>\w+)/', 'email_change_confirm', name='email_change_confirm'),
)

