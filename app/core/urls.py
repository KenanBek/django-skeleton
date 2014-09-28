from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

from reversion.helpers import patch_admin

admin.autodiscover()
patch_admin(User)
patch_admin(Group)

urlpatterns = patterns('',
    url(r'^$', RedirectView.as_view(url='/index', permanent=True)),
    url(r'^', include('website.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
)

