from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from core import abstracts
from .models import Profile, Request


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserNewAdmin(UserAdmin):
    inlines = [ProfileInline, ]


class ProfileAdminAbstract(abstracts.ModelAdminAbstract):
    list_display = ['user', 'website', 'is_verified', ]


class RequestAdmin(abstracts.ModelAdminAbstract):
    list_display = ['user', 'type', 'is_approved', 'key_expires_at', ]
    list_filter = ['user', 'type', 'is_approved', ]


admin.site.unregister(User)
admin.site.register(User, UserNewAdmin)
admin.site.register(Profile, ProfileAdminAbstract)
admin.site.register(Request, RequestAdmin)

