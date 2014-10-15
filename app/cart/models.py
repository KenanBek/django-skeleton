from django.db import models

from core import models as core_models

RATE_VERY_BAD = 1
RATE_BAD = 2
RATE_NORMAL = 3
RATE_GOOD = 4
RATE_VERY_GOOD = 5
RATE_LEVEL = (
    (RATE_VERY_BAD, "Very Bad"),
    (RATE_BAD, "Bad"),
    (RATE_NORMAL, "Normal"),
    (RATE_GOOD, "Good"),
    (RATE_VERY_GOOD, "Very Good"),
)


class Currency(core_models.Model):
    title = models.CharField(max_length=128)

    def __str__(self):
        return self.title


class Manufacturer(core_models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(null=True, blank=True)
    info = models.CharField(max_length=1024, null=True, blank=True)
    image = models.ImageField(upload_to='cart/manufacturer', null=True, blank=True)

    def __str__(self):
        return self.title


class Category(core_models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField(null=True, blank=True)
    info = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.title


class AttributeGroup(core_models.Model):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class Attribute(core_models.Model):
    group = models.ForeignKey(AttributeGroup)
    title = models.CharField(max_length=256)

    def __str__(self):
        return "{0} - {1}".format(self.group.title, self.title)


class Product(core_models.Model):
    is_active = models.BooleanField(default=False)
    category = models.ForeignKey(Category)
    manufacturer = models.ForeignKey(Manufacturer)

    model = models.CharField(max_length=256)
    size = models.CharField(max_length=128, null=True, blank=True)
    weight = models.CharField(max_length=128, null=True, blank=True)
    info = models.CharField(max_length=1024, null=True, blank=True)

    image = models.ImageField(upload_to='cart/product', null=True, blank=True)
    video_code = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return "{0} {1} {2}".format(self.category, self.manufacturer, self.model)


class ProductReview(core_models.Model):
    is_approved = models.BooleanField(default=False)
    product = models.ForeignKey(Product)
    rating = models.IntegerField(choices=RATE_LEVEL, default=RATE_NORMAL)
    comment = models.CharField(max_length=1024)

    class Meta:
        permissions = (
            ('can_approve', 'Can approve review'),
        )


class ProductAttribute(core_models.Model):
    product = models.ForeignKey(Product)
    attribute = models.ForeignKey(Attribute)
    value = models.CharField(max_length=128)


class ProductImage(core_models.Model):
    product = models.ForeignKey(Product)
    image = models.ImageField(upload_to='cart/product')
    info = models.CharField(max_length=1024, null=True, blank=True)


class Shop(core_models.Model):
    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=32)
    slug = models.SlugField(unique=True, null=True, blank=True)
    info = models.CharField(max_length=1024, null=True, blank=True)
    image = models.ImageField(upload_to='cart/shop', null=True, blank=True)

    def __str__(self):
        return self.title


class ShopReview(core_models.Model):
    is_approved = models.BooleanField(default=False)
    shop = models.ForeignKey(Shop)
    rating = models.IntegerField(choices=RATE_LEVEL, default=RATE_NORMAL)
    comment = models.CharField(max_length=1024)

    class Meta:
        permissions = (
            ('can_approve', 'Can approve review'),
        )


class ShopProduct(core_models.Model):
    shop = models.ForeignKey(Shop)
    product = models.ForeignKey(Product)
    currency = models.ForeignKey(Currency)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    quantity = models.IntegerField()
    info = models.CharField(max_length=1024, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

