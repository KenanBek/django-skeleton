from django.conf.urls import patterns, url

urlpatterns = patterns('website.views',
    url(r'$', 'index', name='home_index'),
)

