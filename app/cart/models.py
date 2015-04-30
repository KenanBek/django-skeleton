from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _

from core import abstracts
from core.utils import helpers


def get_cart_file_name(instance, filename):
    return helpers.get_file_filename(instance, filename, "profile")


''' Choices '''

RATING_VERY_BAD = 1
RATING_BAD = 2
RATING_NORMAL = 3
RATING_GOOD = 4
RATING_VERY_GOOD = 5
RATING_CHOICES = (
    (RATING_VERY_BAD, "Very Bad"),
    (RATING_BAD, "Bad"),
    (RATING_NORMAL, "Normal"),
    (RATING_GOOD, "Good"),
    (RATING_VERY_GOOD, "Very Good"),
)

''' Base objects '''


class Currency(abstracts.ModelAbstract):
    title = models.CharField(max_length=128)

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return self.__str__()


class Manufacturer(abstracts.ModelAbstract):
    title = models.CharField(max_length=256)
    slug = models.SlugField(editable=False)
    info = models.CharField(max_length=1024, null=True, blank=True)
    image = models.ImageField(max_length=1024, null=True, blank=True, upload_to=get_cart_file_name)

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        self.slug = helpers.get_slug(self.title)
        super(Manufacturer, self).save(*args, **kwargs)


class Category(abstracts.ModelAbstract):
    title = models.CharField(max_length=256)
    slug = models.SlugField(unique=True, editable=False)
    info = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        self.slug = helpers.get_slug(self.title)
        super(Category, self).save(*args, **kwargs)


class AttributeGroup(abstracts.ModelAbstract):
    title = models.CharField(max_length=256)

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return self.__str__()


class Attribute(abstracts.ModelAbstract):
    group = models.ForeignKey(AttributeGroup)
    title = models.CharField(max_length=256)

    def __str__(self):
        return u"{0} - {1}".format(self.group.title, self.title)

    def __unicode__(self):
        return self.__str__()


''' Product '''


class Product(abstracts.ModelAbstract):
    is_active = models.BooleanField(default=False)
    category = models.ForeignKey(Category)
    manufacturer = models.ForeignKey(Manufacturer)

    model = models.CharField(max_length=256)
    size = models.CharField(max_length=128, null=True, blank=True)
    weight = models.CharField(max_length=128, null=True, blank=True)
    info = models.CharField(max_length=1024, null=True, blank=True)

    image = models.ImageField(max_length=1024, null=True, blank=True, upload_to=get_cart_file_name)
    video_code = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return u"{0}/{1}/{2}".format(self.category, self.manufacturer, self.model)

    def __unicode__(self):
        return self.__str__()


class ProductReview(abstracts.ModelAbstract):
    is_approved = models.BooleanField(default=False)
    product = models.ForeignKey(Product)
    user = models.ForeignKey(User)
    rating = models.IntegerField(choices=RATING_CHOICES, default=RATING_NORMAL)
    comment = models.CharField(max_length=1024)

    def __str__(self):
        return u"User '{0}' reviewed product '{1}' with '{2}' rating".format(self.user, self.product,
            RATING_CHOICES[self.rating][1])

    def __unicode__(self):
        return self.__str__()

    class Meta:
        permissions = (
            ('can_approve', _('Can approve review')),
        )


class ProductAttribute(abstracts.ModelAbstract):
    product = models.ForeignKey(Product)
    attribute = models.ForeignKey(Attribute)
    value = models.CharField(max_length=128)

    def __str__(self):
        return u"Product '{}' attribute {} = {}".format(self.product, self.attribute, self.value)

    def __unicode__(self):
        return self.__str__()


class ProductImage(abstracts.ModelAbstract):
    product = models.ForeignKey(Product)
    image = models.ImageField(max_length=1024, null=True, blank=True, upload_to=get_cart_file_name)
    info = models.CharField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return u"Image for '{0}' product".format(self.product)

    def __unicode__(self):
        return self.__str__()


''' Shop '''


class Shop(abstracts.ModelAbstract):
    is_active = models.BooleanField(default=False)
    title = models.CharField(max_length=32)
    slug = models.SlugField(editable=False)
    info = models.CharField(max_length=1024, null=True, blank=True)
    image = models.ImageField(max_length=1024, null=True, blank=True, upload_to=get_cart_file_name)

    def __str__(self):
        return u"{}".format(self.title)

    def __unicode__(self):
        return self.__str__()

    def save(self, *args, **kwargs):
        self.slug = helpers.get_slug(self.title)
        super(Shop, self).save(*args, **kwargs)


class ShopReview(abstracts.ModelAbstract):
    is_approved = models.BooleanField(default=False)
    shop = models.ForeignKey(Shop)
    user = models.ForeignKey(User)
    rating = models.IntegerField(choices=RATING_CHOICES, default=RATING_NORMAL)
    comment = models.CharField(max_length=1024)

    def __str__(self):
        return u"User '{0}' reviewed shop '{1}' with '{2}' rating".format(self.user, self.product,
            RATING_CHOICES[self.rating][1])

    def __unicode__(self):
        return self.__str__()

    class Meta:
        permissions = (
            ('can_approve', _('Can approve review')),
        )


class ShopProduct(abstracts.ModelAbstract):
    shop = models.ForeignKey(Shop)
    product = models.ForeignKey(Product)
    currency = models.ForeignKey(Currency)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    info = models.CharField(max_length=1024, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return u"Product '{0}' attached to '{1}' shop with '{2} {3}' price".format(self.product, self.shop, self.price,
            self.currency)

    def __unicode__(self):
        return self.__str__()

