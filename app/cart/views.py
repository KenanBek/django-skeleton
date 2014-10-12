from django.shortcuts import render
import models


def index(request, template='bootstrap3/cart/index.html', context={}):
    last_products = models.Product.objects.all()
    context['last_products'] = last_products
    return render(request, template, context)

