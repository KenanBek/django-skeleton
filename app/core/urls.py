from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.views.decorators.cache import cache_page
from django.templatetags.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemaps_views

from core import sitemaps as application_sitemaps

admin.autodiscover()

# Root url patterns
urlpatterns = patterns('',
    # Admin and 3rd party applications
    url(r'^language/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^select2/', include('django_select2.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # Static
    url(r'^$', TemplateView.as_view(template_name='user/home.html'), name='index'),
    url(r'^about/$', TemplateView.as_view(template_name='user/home.html'), name='about'),
    # Applications
    url(r'^system/', include('system.urls')),
    url(r'^account/', include('account.urls')),
    url(r'^website/', include('website.urls')),
    url(r'^cart/', include('cart.urls')),
    # SEO
    url(r'^favicon\.ico$', RedirectView.as_view(url=static('favicon.ico'), permanent=True), name="favicon.ico"),
    url(r'^robots\.txt$', RedirectView.as_view(url=static('robots.txt'), permanent=True), name="robots.txt"),
    url(r'^sitemap\.xml$',
        cache_page(10000)(sitemaps_views.index),
        {'sitemaps': application_sitemaps.sitemaps_dict}),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        cache_page(10000)(sitemaps_views.sitemap),
        {'sitemaps': application_sitemaps.sitemaps_dict}),
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
handler400 = 'system.views.error_400'  # Request cannot be fulfilled due to bad syntax
handler403 = 'system.views.error_403'  # Server refuses to respond to request
handler404 = 'system.views.error_404'  # Requested resource could not be found
handler500 = 'system.views.error_500'  # Server generic error message

