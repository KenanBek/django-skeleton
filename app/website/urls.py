from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
    url(r'^index/$', 'index', name='website_index'),
    url(r'^about/$', 'about', name='website_about'),
    url(r'^contact/$', 'contact', name='website_contact'),
    url(r'^contact/document/$', 'document', name='website_document'),

    url(r'^page/(?P<page_slug>[\w-]+)/$', 'page', name='website_page'),
    url(r'^post/(?P<post_id>[0-9]+)-(?P<post_slug>[\w-]+)/$', 'post', name='website_post'),
    url(r'^search/$', 'search', name='website_search'),
    url(r'^subscribe/$', 'subscribe', name='website_subscribe'),
)

