from django.db import models

from core import models as core_models


class Currency(core_models.Model):
    title = models.CharField(max_length=128)


class Manufacturer(core_models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField()
    info = models.CharField(max_length=1024)
    image = models.ImageField(upload_to='cart/manufacturer', null=True, blank=True)


class Category(core_models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField()
    info = models.CharField(max_length=1024)


class AttributeGroup(core_models.Model):
    title = models.CharField(max_length=256)


class Attribute(core_models.Model):
    group = models.ForeignKey(AttributeGroup)
    title = models.CharField(max_length=256)


class Product(core_models.Model):
    is_active = models.BooleanField()
    category = models.ForeignKey(Category)
    manufacturer = models.ForeignKey(Manufacturer)

    model = models.CharField(max_length=256)
    size = models.CharField(max_length=128)
    weight = models.CharField(max_length=128)

    video_link = models.CharField(max_length=1024)


class ProductImage(core_models.Model):
    image = models.ImageField(upload_to='cart/product')
    info = models.CharField(max_length=1024)


class ProductReview(core_models.Model):
    pass

    product = models.ForeignKey(Product)


class Shop(core_models.Model):
    is_active = models.BooleanField()
    title = models.CharField(max_length=32)
    slug = models.SlugField(unique=True)
    info = models.CharField(max_length=1024)


class ShopReview(core_models.Model):
    pass


class ShopProductPrice(core_models.Model):
    shop = models.ForeignKey(Shop)
    product = models.ForeignKey(Product)
    currency = models.ForeignKey(Currency)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()
    info = models.CharField(max_length=1024)
    url = models.URLField()

