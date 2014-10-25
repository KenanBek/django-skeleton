"""
Base model classes. Used in other applications.
"""

from django.db import models
from reversion import VersionAdmin
#from guardian.admin import GuardedModelAdmin

PUBLISHED = "Published"
HIDDEN = "Hidden"
MODEL_STATUS = (
    (PUBLISHED, "Published"),
    (HIDDEN, "Hidden"),
)


class Model(models.Model):
    added_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    modified_at = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        abstract = True


class ModelAdmin(VersionAdmin):
    pass

