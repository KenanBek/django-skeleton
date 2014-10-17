from django.db import models

from core import models as core_models
from core.models import MODEL_STATUS, PUBLISHED


# Slider


class Slider(core_models.Model):
    status = models.CharField(max_length=9, choices=MODEL_STATUS, default=PUBLISHED)
    title = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Slide(core_models.Model):
    status = models.CharField(max_length=9, choices=MODEL_STATUS, default=PUBLISHED)
    title = models.CharField(max_length=32)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='website/slider/', null=True, blank=True)
    related_slider = models.ForeignKey(Slider)

    def __str__(self):
        return self.title


# Page


class Widget(core_models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField()
    featured_image = models.ImageField(upload_to='website/widget/', null=True, blank=True)
    link_title = models.CharField(max_length=32, null=True, blank=True)
    link_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.title


class Page(core_models.Model):
    status = models.CharField(max_length=9, choices=MODEL_STATUS, default=PUBLISHED)
    title = models.CharField(max_length=32)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    widgets = models.ManyToManyField(Widget, null=True, blank=True)
    featured_image = models.ImageField(upload_to='website/page/', null=True, blank=True)
    related_slider = models.ForeignKey(Slider, null=True, blank=True)

    def get_widgets(self):
        return self.widgets.all()

    def __str__(self):
        return self.title


# Post


class Category(core_models.Model):
    title = models.CharField(max_length=32)
    slug = models.SlugField(unique=True)
    description = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self):
        return self.title


class Post(core_models.Model):
    status = models.CharField(max_length=9, choices=MODEL_STATUS, default=PUBLISHED)
    title = models.CharField(max_length=32)
    slug = models.SlugField(unique=True)
    short_content = models.CharField(max_length=512)
    full_content = models.TextField()
    categories = models.ManyToManyField(Category)
    featured_image = models.ImageField(upload_to='website/post/', null=True, blank=True)
    related_slider = models.ForeignKey(Slider, null=True, blank=True)

    def __str__(self):
        return self.title


# Subscriber & Document


class Subscriber(core_models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField(unique=True)

    def __str__(self):
        return "{0} ({1})".format(self.name, self.email)


class Document(core_models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()
    short_description = models.CharField(max_length=128)
    document_file = models.FileField(upload_to='website/document/')


# Contact


class Contact(core_models.Model):
    name = models.CharField(max_length=32)
    email = models.EmailField()
    subject = models.CharField(max_length=32)
    message = models.TextField()

