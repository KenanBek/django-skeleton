from django.conf.urls import patterns, url
from django.views.generic import RedirectView

urlpatterns = patterns('account.views',
    # General
    url(r'^$', RedirectView.as_view(url='/account/index', permanent=True)),
    url(r'^index/$', 'index', name='account_index'),
    url(r'^login/$', 'login', name='account_login'),
    url(r'^register/$', 'register', name='account_register'),
    url(r'^logout/$', 'logout', name='account_logout'),

    url(r'^login/facebook/$', 'login_facebook', name='account_login_facebook'),

    url(r'^auth/$', 'auth', name='account_auth'),
    url(r'^auth/login/$', 'auth_login', name='account_auth_login'),
    url(r'^auth/register/$', 'auth_register', name='account_auth_register'),
    url(r'^auth/google/$', 'auth_google', name='account_auth_google'),
    url(r'^auth/facebook/$', 'auth_facebook', name='account_auth_facebook'),
    url(r'^auth/twitter/$', 'auth_twitter', name='account_auth_twitter'),
    url(r'^auth/logout/$', 'auth_twitter', name='account_auth_logout'),
)

