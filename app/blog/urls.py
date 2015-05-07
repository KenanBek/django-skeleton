from django.conf.urls import patterns, url, include
from rest_framework.routers import DefaultRouter

from . import views
from . import api

api_router = DefaultRouter()
api_router.register(r'pages', api.PageViewSet)
api_router.register(r'posts', api.PostViewSet)

beep_urlpatterns = patterns('',
    url(r'^$', views.BeepList.as_view(), name='blog_beep_list'),
    url(r'^new/$', views.BeepCreate.as_view(), name='blog_beep_new'),
    url(r'^edit/(?P<pk>\d+)/$', views.BeepUpdate.as_view(), name='blog_beep_edit'),
    url(r'^view/(?P<pk>\d+)/$', views.BeepDetail.as_view(), name='blog_beep_detail'),
    url(r'^delete/(?P<pk>\d+)/$', views.BeepDelete.as_view(), name='blog_beep_delete'),
)

urlpatterns = patterns('blog.views',
    # General
    url(r'^index/$', 'index', name='blog_index'),
    url(r'^contact/$', 'contact', name='blog_contact'),
    url(r'^contact/document/$', 'document', name='blog_document'),
    url(r'^subscribe/$', 'subscribe', name='blog_subscribe'),
    # Pages
    url(r'^pages/$', 'pages', name='blog_pages'),
    url(r'^page/(?P<page_slug>[\w-]+)/$', 'page', name='blog_page'),
    # Posts
    url(r'^posts/$', 'posts', name='blog_posts'),
    url(r'^post/(?P<post_id>[0-9]+)/(?P<post_slug>[\w-]+)/$', 'post', name='blog_post'),
    # Beep
    url(r'^beep/', include(beep_urlpatterns)),
    # Search
    url(r'^search/$', 'search', name='blog_search'),
    # API
    url(r'^api/', include(api_router.urls)),
)

