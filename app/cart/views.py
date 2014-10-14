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

    for shop_product in related_shop_products:
        shop_products.append(shop_product.product)

    context['shop_item'] = shop_item
    context['shop_products'] = shop_products
    return render(request, template, context)

