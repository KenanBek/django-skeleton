from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.conf.urls import patterns, include, url

from reversion.helpers import patch_admin

admin.autodiscover()
patch_admin(User)
patch_admin(Group)

urlpatterns = patterns('',
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('website.urls')),
)

