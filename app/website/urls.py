from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

from website import api

api_router = DefaultRouter()
api_router.register(r'pages', api.PageViewSet)
api_router.register(r'posts', api.PostViewSet)

urlpatterns = patterns('website.views',
    # General
    url(r'^index/$', 'index', name='website_index'),
    url(r'^contact/$', 'contact', name='website_contact'),
    url(r'^contact/document/$', 'document', name='website_document'),
    url(r'^subscribe/$', 'subscribe', name='website_subscribe'),
    # Pages
    url(r'^pages/$', 'pages', name='website_pages'),
    url(r'^page/(?P<page_slug>[\w-]+)/$', 'page', name='website_page'),
    # Posts
    url(r'^posts/$', 'posts', name='website_posts'),
    url(r'^post/(?P<post_id>[0-9]+)/(?P<post_slug>[\w-]+)/$', 'post', name='website_post'),
    # Search
    url(r'^search/$', 'search', name='website_search'),
    # API
    url(r'^api/', include(api_router.urls)),
)

