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

