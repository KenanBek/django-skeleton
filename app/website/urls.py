from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

import api

api_router = DefaultRouter()
api_router.register(r'pages', api.PageViewSet)
api_router.register(r'posts', api.PostViewSet)

urlpatterns = patterns('website.views',
    # General
    url(r'^index/$', 'index', name='website_index'),
    url(r'^about/$', 'about', name='website_about'),
    url(r'^contact/$', 'contact', name='website_contact'),
    url(r'^contact/document/$', 'document', name='website_document'),
    url(r'^subscribe/$', 'subscribe', name='website_subscribe'),
    # Page and Post
    url(r'^page/(?P<page_slug>[\w-]+)/$', 'page', name='website_page'),
    url(r'^post/(?P<post_id>[0-9]+)-(?P<post_slug>[\w-]+)/$', 'post', name='website_post'),
    # Search
    url(r'^search/$', 'search', name='website_search'),
    # API
    url(r'^api/', include(api_router.urls)),
)

