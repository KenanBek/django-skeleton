from django.conf.urls import patterns, url

urlpatterns = patterns('moderator.views',
    url(r'^$', 'index', name='index'),
)

