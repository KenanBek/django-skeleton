from django.contrib.auth.decorators import login_required
from django.db import models
from django.contrib import admin
from django.views.decorators.cache import never_cache


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


class LogicAbstract(object):
    def __init__(self, request):
        self.request = request

    def grab_get_param(self, param):
        return self.request.GET.get(param, None)

    def grab_post_param(self, param):
        return self.request.POST.get(param, None)


''' Class Based Views '''


class NeverCacheMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(NeverCacheMixin, cls).as_view(**initkwargs)
        return never_cache(view)


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)

