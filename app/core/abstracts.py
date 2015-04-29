from django.db import models
from django.contrib import admin


class ModelAbstract(models.Model):
    added_at = models.DateTimeField(auto_now_add=True, editable=False, null=True)
    modified_at = models.DateTimeField(auto_now=True, editable=False, null=True)

    class Meta:
        abstract = True


class ModelAdminAbstract(admin.ModelAdmin):
    pass


class ModelReadOnlyAdminAbstract(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False