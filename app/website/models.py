from django.db import models

from core import models as core_models


class Widget(core_models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField()

    def __str__(self):
        return self.title


class Page(core_models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=32)
    content = models.TextField()
    widgets = models.ManyToManyField(Widget)

    def get_widgets(self):
        return self.widgets.all()

    def __str__(self):
        return self.title


class Category(core_models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=512)

    def __str__(self):
        return self.title


class Post(core_models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=32)
    short_content = models.CharField(max_length=512)
    full_content = models.TextField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

