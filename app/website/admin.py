from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django_select2 import fields

from core import models as core_models
from website import models


class WidgetAdminAbstract(core_models.ModelAdminAbstract):
    list_display = ['title', 'related_page_names']

    def related_page_names(self, obj):
        return ",\n".join([page.title for page in obj.page_set.all()])


# Page


class PageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = models.Page
        fields = '__all__'


class PageAdminAbstract(core_models.ModelAdminAbstract):
    form = PageAdminForm

    list_filter = ['status']
    list_display = ['slug', 'title', 'related_widget_names', 'related_slider', 'status']

    def related_widget_names(self, obj):
        return ",\n".join([widget.title for widget in obj.widgets.all()])


# Category


class CategoryAdminForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = models.Category
        fields = '__all__'


class CategoryAdminAbstract(core_models.ModelAdminAbstract):
    form = CategoryAdminForm

    list_display = ['title', 'slug', 'related_post_names']

    def related_post_names(self, obj):
        return ",\n".join([post.title for post in obj.post_set.all()])


# Post


class CategoryChoice(fields.AutoModelSelect2MultipleField):
    queryset = models.Category.objects
    search_fields = ['title__icontains', ]


class PostAdminForm(forms.ModelForm):
    short_content = forms.CharField(widget=forms.Textarea())
    full_content = forms.CharField(widget=CKEditorWidget())
    categories = CategoryChoice()

    class Meta:
        model = models.Post
        fields = '__all__'


class PostAdminAbstract(core_models.ModelAdminAbstract):
    form = PostAdminForm

    list_filter = ['added_at', 'status', 'categories']
    list_display = ['added_at', 'slug', 'title', 'short_content', 'related_category_names', 'related_slider', 'status']

    def related_category_names(self, obj):
        return ",\n".join([category.title for category in obj.categories.all()])


# Slider


class SlideInline(admin.StackedInline):
    model = models.Slide
    extra = 1


class SliderAdminAbstract(core_models.ModelAdminAbstract):
    list_display = ['title', 'status']
    inlines = [SlideInline, ]


# Subscriber & Document


class SubscriberAdminAbstract(core_models.ModelAdminAbstract):
    list_filter = ['added_at', 'email']
    list_display = ['added_at', 'name', 'email']


class DocumentAdminAbstract(core_models.ModelAdminAbstract):
    list_filter = ['added_at', 'email']
    list_display = ['added_at', 'name', 'email']


# Contact


class ContactAdminAbstract(core_models.ModelAdminAbstract):
    list_filter = ['added_at', 'email']
    list_display = ['added_at', 'name', 'email', 'subject']


admin.site.register(models.Widget, WidgetAdminAbstract)
admin.site.register(models.Page, PageAdminAbstract)
admin.site.register(models.Category, CategoryAdminAbstract)
admin.site.register(models.Post, PostAdminAbstract)
admin.site.register(models.Slider, SliderAdminAbstract)
admin.site.register(models.Subscriber, SubscriberAdminAbstract)
admin.site.register(models.Document, DocumentAdminAbstract)
admin.site.register(models.Contact, ContactAdminAbstract)

