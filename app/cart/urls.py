from django.conf.urls import patterns, url
from django.views.generic import RedirectView

urlpatterns = patterns('cart.views',
    url(r'^$', RedirectView.as_view(url='/cart/index', permanent=True), name='index'),
    url(r'^index/$', 'index', name='cart_index'),
)

