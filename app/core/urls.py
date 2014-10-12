from django.contrib import admin
#from django.contrib.auth.models import User, Group
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView

#from reversion.helpers import patch_admin

admin.autodiscover()
#patch_admin(User)
#patch_admin(Group)

# Root url patterns
urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^$', RedirectView.as_view(url='/index', permanent=True), name='index'),
    url(r'^', include('website.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^cart/', include('cart.urls')),
)

# Serve static files
urlpatterns += patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
)

# Serve media files
urlpatterns += patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

# Configure error handlers
handler400 = 'error.views.error_400'  # Request cannot be fulfilled due to bad syntax
handler403 = 'error.views.error_403'  # Server refuses to respond to request
handler404 = 'error.views.error_404'  # Requested resource could not be found
handler500 = 'error.views.error_500'  # Server generic error message

