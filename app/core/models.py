"""
Base model classes. Used in other applications.
"""

from django.db import models
from django.contrib import admin


class ModelAbstract(models.Model):
    added_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    modified_at = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        abstract = True


class ModelAdmin(admin.ModelAdmin):
    pass

