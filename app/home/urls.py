from django.conf.urls import patterns, url

urlpatterns = patterns('home.views',
    url(r'$', 'index', name='home_index'),
)

