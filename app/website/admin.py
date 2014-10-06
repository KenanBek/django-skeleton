from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget

from app.core import models as core_models
import models


# Widget


class WidgetAdmin(core_models.ModelAdmin):
    list_display = ['title', 'related_page_names']

    def related_page_names(self, obj):
        return ",\n".join([page.title for page in obj.page_set.all()])


# Page


class PageAdmin(core_models.ModelAdmin):
    list_filter = ['status']
    list_display = ['slug', 'title', 'related_widget_names', 'related_slider', 'status']

    def related_widget_names(self, obj):
        return ",\n".join([widget.title for widget in obj.widgets.all()])


# Category


class CategoryAdmin(core_models.ModelAdmin):
    list_display = ['slug', 'title', 'related_post_names']

    def related_post_names(self, obj):
        return ",\n".join([post.title for post in obj.post_set.all()])


# Post

class PostAdminForm(forms.ModelForm):
    full_content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = models.Post


class PostAdmin(core_models.ModelAdmin):
    list_filter = ['added_at', 'status']
    list_display = ['added_at', 'slug', 'title', 'short_content', 'related_category_names', 'related_slider', 'status']
    form = PostAdminForm

    def related_category_names(self, obj):
        return ",\n".join([category.title for category in obj.categories.all()])


# Slider


class SlideInline(admin.StackedInline):
    model = models.Slide
    extra = 1


class SliderAdmin(core_models.ModelAdmin):
    list_display = ['title', 'status']
    inlines = [SlideInline, ]


# Subscriber & Document


class SubscriberAdmin(core_models.ModelAdmin):
    list_filter = ['added_at', 'email']
    list_display = ['added_at', 'name', 'email']


class DocumentAdmin(core_models.ModelAdmin):
    list_filter = ['added_at', 'email']
    list_display = ['added_at', 'name', 'email']


# Contact


class ContactAdmin(core_models.ModelAdmin):
    list_filter = ['added_at', 'email']
    list_display = ['added_at', 'name', 'email', 'subject']


admin.site.register(models.Widget, WidgetAdmin)
admin.site.register(models.Page, PageAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Slider, SliderAdmin)
admin.site.register(models.Subscriber, SubscriberAdmin)
admin.site.register(models.Document, DocumentAdmin)
admin.site.register(models.Contact, ContactAdmin)

