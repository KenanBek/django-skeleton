from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from django_select2 import fields

from core import abstracts
from . import models





# Slider


class SlideInline(admin.TabularInline):
    model = models.Slide
    extra = 1


class SliderAdmin(abstracts.ModelAdminAbstract):
    list_display = ['title', 'status']
    inlines = [SlideInline, ]


admin.site.register(models.Slider, SliderAdmin)


# Page and Post actions


def publish_item(model_admin, request, queryset):
    queryset.update(status=models.ITEM_STATUS_PUBLISHED)


publish_item.short_description = "Publish selected items"


def hide_item(model_admin, request, queryset):
    queryset.update(status=models.ITEM_STATUS_HIDDEN)


hide_item.short_description = "Hide selected items"


# Page


class PageAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = models.Page
        fields = '__all__'


class PageAdmin(abstracts.ModelAdminAbstract):
    form = PageAdminForm

    list_filter = ['status']
    list_display = ['slug', 'title', 'related_widget_names', 'related_slider', 'status']

    actions = [publish_item, hide_item, ]

    def related_widget_names(self, obj):
        return ",\n".join([widget.title for widget in obj.widgets.all()])


class WidgetAdmin(abstracts.ModelAdminAbstract):
    list_display = ['title', 'related_page_names']

    def related_page_names(self, obj):
        return ",\n".join([page.title for page in obj.page_set.all()])


admin.site.register(models.Widget, WidgetAdmin)
admin.site.register(models.Page, PageAdmin)


# Post


class CategoryAdminForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = models.Category
        fields = '__all__'


class CategoryAdmin(abstracts.ModelAdminAbstract):
    form = CategoryAdminForm

    list_display = ['title', 'slug', 'related_post_names']

    def related_post_names(self, obj):
        return ",\n".join([post.title for post in obj.post_set.all()])


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


class PostAdmin(abstracts.ModelAdminAbstract):
    form = PostAdminForm

    list_filter = ['added_at', 'status', 'categories']
    list_display = ['added_at', 'slug', 'title', 'short_content', 'related_category_names', 'related_slider', 'status']

    actions = [publish_item, hide_item, ]

    def related_category_names(self, obj):
        return ",\n".join([category.title for category in obj.categories.all()])


admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Post, PostAdmin)


# Beep


class BeepAdmin(abstracts.ModelAdminAbstract):
    search_fields = ['text', ]
    list_filter = ['user', ]
    list_display = ['text', 'length', 'user', 'modified_at', ]


admin.site.register(models.Beep, BeepAdmin)


# Subscriber & Document


class SubscriberAdmin(abstracts.ModelAdminAbstract):
    list_filter = ['added_at', 'email']
    list_display = ['added_at', 'name', 'email']


class DocumentAdmin(abstracts.ModelAdminAbstract):
    list_filter = ['added_at', 'email']
    list_display = ['added_at', 'name', 'email']


admin.site.register(models.Subscriber, SubscriberAdmin)
admin.site.register(models.Document, DocumentAdmin)


# Contact


class ContactAdmin(abstracts.ModelAdminAbstract):
    list_filter = ['added_at', 'email']
    list_display = ['added_at', 'name', 'email', 'subject']


admin.site.register(models.Contact, ContactAdmin)

