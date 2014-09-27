from django.db import models

from core import models as core_models


class Page(core_models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=32)
    content = models.TextField()


class Category(core_models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=512)


class Post(core_models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=32)
    short_content = models.CharField(max_length=512)
    full_content = models.TextField()
    categories = models.ManyToManyField(Category)

