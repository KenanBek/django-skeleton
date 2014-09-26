from django.db import models

from core import models as core_models


class Page(core_models.Model):
    slug = models.SlugField(unique=True)
    title = models.CharField(max_length=32)
    content = models.TextField()

