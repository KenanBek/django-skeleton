from django.conf.urls import patterns, url
from django.views.generic import RedirectView

urlpatterns = patterns('cart.views',
    url(r'^$', RedirectView.as_view(url='/cart/index', permanent=True)),
    url(r'^index/$', 'index', name='cart_index'),
    url(r'^product/(?P<product_id>[0-9]+)/$', 'product', name='cart_product'),
    url(r'^product/review/(?P<product_id>[0-9]+)/$', 'product_review', name='cart_product_review'),
    url(r'^shop/(?P<shop_id>[0-9]+)/$', 'shop', name='cart_shop'),
    url(r'^shop/review/(?P<shop_id>[0-9]+)/$', 'shop_review', name='cart_shop_review'),
)

