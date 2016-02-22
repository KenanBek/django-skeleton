from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from core import abstracts
from .models import Profile, Request, REQUEST_TYPE_ACCOUNT, REQUEST_TYPE_EMAIL, REQUEST_TYPE_PASSWORD


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'profile'


class UserNewAdmin(UserAdmin):
    inlines = [ProfileInline, ]


'''Profile Actions '''


class ProfileActions(object):
    @staticmethod
    def verify_selected_profiles(model_admin, request, queryset):
        rows_updated = queryset.update(is_verified=True)
        if rows_updated == 1:
            message_bit = "1 profile was"
        else:
            message_bit = "%s profiles were" % rows_updated
        model_admin.message_user(request, "%s successfully marked as verified." % message_bit)


    @staticmethod
    def unverify_selected_profiles(model_admin, request, queryset):
        rows_updated = queryset.update(is_verified=False)
        if rows_updated == 1:
            message_bit = "1 profile was"
        else:
            message_bit = "%s profiles were" % rows_updated
        model_admin.message_user(request, "%s successfully marked as unverified." % message_bit)


class ProfileAdminAbstract(abstracts.ModelAdminAbstract):
    list_display = ['user', 'website', 'is_verified', ]
    actions = [ProfileActions.verify_selected_profiles, ProfileActions.unverify_selected_profiles]


'''Request Actions '''


class RequestActions(object):
    @staticmethod
    def approve_selected_requests(model_admin, request, queryset):
        if (queryset.filter(type=REQUEST_TYPE_ACCOUNT)):
            for q in queryset:
                q.user.profile.is_verified = True
                q.user.profile.save()
            rows_updated = queryset.update(is_approved=True)
            if rows_updated == 1:
                message_bit = "1 request was"
            else:
                message_bit = "%s requests were" % rows_updated
            model_admin.message_user(request, "%s successfully marked as approved." % message_bit)
        elif (queryset.filter(type=REQUEST_TYPE_EMAIL)):
            for q in queryset:
                q.user.email = q.str_field_1
                q.user.save()
                q.user.profile.is_verified = True
                q.user.profile.save()
            queryset.update(is_approved=True)
        elif (queryset.filter(type=REQUEST_TYPE_PASSWORD)):
            for q in queryset:
                q.user.set_unusable_password()
                q.user.save()
            queryset.update(is_approved=True)


    @staticmethod
    def refuse_selected_requests(model_admin, request, queryset):
        if (queryset.filter(type=REQUEST_TYPE_ACCOUNT)):
            for q in queryset:
                q.user.profile.is_verified = False
                q.user.profile.save()
            rows_updated = queryset.update(is_approved=False)
            if rows_updated == 1:
                message_bit = "1 request was"
            else:
                message_bit = "%s requests were" % rows_updated
            model_admin.message_user(request, "%s successfully marked as refused." % message_bit)
        elif (queryset.filter(type=REQUEST_TYPE_EMAIL)):
            for q in queryset:
                q.user.email = q.str_field_2
                q.user.save()
                q.user.profile.is_verified = False
                q.user.profile.save()
            queryset.update(is_approved=False)
        elif (queryset.filter(type=REQUEST_TYPE_PASSWORD)):
            for q in queryset:
                q.user.set_password("12345")
                q.user.save()
            queryset.update(is_approved=False)

            # rows_updated = queryset.update(is_approved=False)
            # if rows_updated == 1:
            # message_bit = "1 request was"
            # else:
            # message_bit = "%s requests were" % rows_updated
            # model_admin.message_user(request, "%s successfully marked as refused." % message_bit)


class RequestAdmin(abstracts.ModelAdminAbstract):
    list_display = ['user', 'type', 'is_approved', 'activation_key', 'str_field_1', 'str_field_2', 'dec_field_1',
                    'dec_field_2', 'bool_field_1', 'bool_field_2', 'key_expires_at', ]
    list_filter = ['user', 'type', 'is_approved', ]
    actions = [RequestActions.approve_selected_requests, RequestActions.refuse_selected_requests]


admin.site.unregister(User)
admin.site.register(User, UserNewAdmin)
admin.site.register(Profile, ProfileAdminAbstract)
admin.site.register(Request, RequestAdmin)

