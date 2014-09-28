"""
Base model classes. Used in other applications.
"""

from django.db import models
import reversion

DRAFT = "Draft"
PUBLISHED = "Published"
HIDDEN = "Hidden"
MODEL_STATUS = (
    (DRAFT, "Draft"),
    (PUBLISHED, "Published"),
    (HIDDEN, "Hidden")
)


class Model(models.Model):
    added_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    modified_at = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        abstract = True


class ModelAdmin(reversion.VersionAdmin):
    pass

