from django.conf import settings
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView, RedirectView
from django.views.decorators.cache import cache_page
from django.templatetags.static import static
from django.contrib import admin
from django.contrib.sitemaps import views as sitemaps_views

from . import sitemaps as core_sitemaps

admin.autodiscover()

# Root url patterns
urlpatterns = patterns('',
    # Admin and 3rd party applications
    url(r'^admin/', include(admin.site.urls)),
    url(r'^plugin/ckeditor/', include('ckeditor.urls')),
    url(r'^plugin/select/', include('django_select2.urls')),
    url(r'^api/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^social/', include('social.apps.django_app.urls', namespace='social')),
    # Core
    url(r'^$', 'core.views.home', name='home'),
    url(r'^about/$', 'core.views.about', name='about'),
    url(r'^error/400/$', 'core.views.error_400', name='error_400'),
    url(r'^error/403/$', 'core.views.error_403', name='error_403'),
    url(r'^error/404/$', 'core.views.error_404', name='error_404'),
    url(r'^error/500/$', 'core.views.error_500', name='error_500'),
    url(r'^static-page/$', TemplateView.as_view(template_name='user/core/static_page.html'), name='static_page'),
    url(r'^debug/$', 'core.views.debug', name='debug'),
    url(r'^language/(?P<code>\w+)/$', 'core.views.language', name='language'),
    url(r'^moderator/', include('moderator.urls', namespace='moderator')),
    url(r'^search/$', 'core.views.search', name='search'),
    url(r'^search_autocomplete/$', 'core.logic.search_autocomplete', name='search_autocomplete'),
    url(r'^search/search_autocomplete/$', 'core.logic.search_autocomplete', name='search_autocomplete'),
    # Applications
    url(r'^account/', include('account.urls')),
    url(r'^blog/', include('blog.urls')),
    # SEO
    url(r'^favicon\.ico$', RedirectView.as_view(url=static('favicon.ico'), permanent=True), name="favicon.ico"),
    url(r'^robots\.txt$', RedirectView.as_view(url=static('robots.txt'), permanent=True), name="robots.txt"),
    url(r'^sitemap\.xml$',
        cache_page(60 * 10)(sitemaps_views.index),  # cache for 10 minutes
        {'sitemaps': core_sitemaps.sitemaps_dict}),
    url(r'^sitemap-(?P<section>.+)\.xml$',
        cache_page(60 * 10)(sitemaps_views.sitemap),  # cache for 10 minutes
        {'sitemaps': core_sitemaps.sitemaps_dict}),
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
handler400 = 'core.views.error_400'  # Request cannot be fulfilled due to bad syntax
handler403 = 'core.views.error_403'  # Server refuses to respond to request
handler404 = 'core.views.error_404'  # Requested resource could not be found
handler500 = 'core.views.error_500'  # Server generic error message

