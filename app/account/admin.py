from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

from core import abstracts
from . import models
from .models import Profile, Request


'''Profile Actions'''


class ProfileActions(object):
    @staticmethod
    def verify_selected_profiles(model_admin, request, queryset):
        queryset.update(is_verified=True)

    @staticmethod
    def unverify_selected_profiles(model_admin, request, queryset):
        queryset.update(is_verified=False)



class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserNewAdmin(UserAdmin):
    inlines = (ProfileInline, )


class ProfileAdminAbstract(abstracts.ModelAdminAbstract):
    list_display = ('user', 'website', 'is_verified')
    actions = [ProfileActions.verify_selected_profiles, ProfileActions.unverify_selected_profiles]


'''Request Actions'''


class RequestActions(object):
    @staticmethod
    def approve_selected_requests(model_admin, request, queryset):
        queryset.update(is_approved=True)

    @staticmethod
    def refuse_selected_requests(model_admin, request, queryset):
        queryset.update(is_approved=False)

class RequestAdmin(abstracts.ModelAdminAbstract):
    list_display = ('user', 'type', 'is_approved', 'key_expires_at')
    list_filter = ('user', 'type', 'is_approved',)
    actions = [RequestActions.approve_selected_requests, RequestActions.refuse_selected_requests]




admin.site.unregister(User)
admin.site.register(User, UserNewAdmin)
admin.site.register(Profile, ProfileAdminAbstract)
admin.site.register(Request, RequestAdmin)

