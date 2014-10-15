from django.shortcuts import render

import models


def index(request, template='bootstrap3/cart/index.html', context={}):
    last_products = models.Product.objects.all()
    context['last_products'] = last_products
    return render(request, template, context)


def product(request, product_id, template='bootstrap3/cart/product.html', context={}):
    product_item = models.Product.objects.get(pk=product_id)
    context['product_item'] = product_item
    return render(request, template, context)


def shop(request, shop_id, template='bootstrap3/cart/shop.html', context={}):
    shop_item = models.Shop.objects.get(pk=shop_id)
    shop_products = []
    related_shop_products = models.ShopProduct.objects.filter(shop=shop_item)

    # calculate rate
    shop_rate = 0
    shop_rate_sum = 0
    shop_rate_count = 0
    for shopreview in shop_item.shopreview_set.all():
        shop_rate_sum += shopreview.rating
        shop_rate_count += 1
        shop_rate = int(shop_rate_sum / shop_rate_count)

    for shop_product in related_shop_products:
        shop_products.append(shop_product.product)

    context['shop_item'] = shop_item
    context['shop_rate'] = range(shop_rate)
    context['shop_products'] = shop_products
    return render(request, template, context)

