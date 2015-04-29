from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
from ckeditor.widgets import CKEditorWidget

from core import abstracts
from cart import models

''' Product '''


class ProductAttributeInline(admin.TabularInline):
    model = models.ProductAttribute
    suit_classes = 'suit-tab suit-tab-attributes'
    extra = 10


class ProductImageInlineForm(forms.ModelForm):
    info = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = models.ProductImage
        fields = '__all__'


class ProductImageInline(admin.StackedInline):
    model = models.ProductImage
    suit_classes = 'suit-tab suit-tab-images'
    form = ProductImageInlineForm
    extra = 6


class ProductAdminForm(forms.ModelForm):
    info = forms.CharField(widget=CKEditorWidget())
    video_code = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = models.Product
        fields = '__all__'


class ProductAdminAbstract(abstracts.ModelAdminAbstract):
    form = ProductAdminForm
    list_display = ['category', 'manufacturer', 'model', 'is_active', ]
    list_filter = ['category', 'manufacturer', ]
    inlines = [ProductAttributeInline, ProductImageInline, ]
    fieldsets = [
        ('Relations', {
            'classes': ('suit-tab suit-tab-general',),
            'description': _('Product relations'),
            'fields': ['is_active', 'category', 'manufacturer', ]
        }),
        ('General', {
            'classes': ('suit-tab suit-tab-general',),
            'description': _('Product general information'),
            'fields': ['model', 'size', 'weight', 'info', ]
        }),
        ('Media', {
            'classes': ('suit-tab suit-tab-general',),
            'description': _('Related media sources'),
            'fields': ['image', 'video_code', ]
        }),
    ]
    suit_form_tabs = (
        ('general', 'General'),
        ('attributes', 'Attributes'),
        ('images', 'Images'),
    )


''' Shop Product '''


class ShopProductInlineForm(forms.ModelForm):
    info = forms.CharField(widget=forms.Textarea(), required=False)

    class Meta:
        model = models.ShopProduct
        fields = '__all__'


class ShopProductInline(admin.StackedInline):
    model = models.ShopProduct
    form = ShopProductInlineForm
    suit_classes = 'suit-tab suit-tab-products'
    exclude = ['url', ]
    extra = 20


class ShopProductAdminAbstract(abstracts.ModelAdminAbstract):
    list_display = ['shop', 'product', 'currency', 'price', 'quantity', ]
    list_filter = ['shop', 'product', ]


''' Shop '''


class ShopAdminForm(forms.ModelForm):
    info = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = models.Shop
        fields = '__all__'


class ShopAdminAbstract(abstracts.ModelAdminAbstract):
    form = ShopAdminForm
    list_display = ['title', 'is_active', ]
    inlines = [ShopProductInline, ]
    fieldsets = [
        ('General', {
            'classes': ('suit-tab suit-tab-general',),
            'description': _('Shop general information'),
            'fields': ['is_active', 'title', 'slug', 'info']
        }),
        ('Media', {
            'classes': ('suit-tab suit-tab-general',),
            'description': _('Shop media files'),
            'fields': ['image', ]
        }),
    ]
    suit_form_tabs = (
        ('general', 'General'),
        ('products', 'Products'),
    )


''' Reviews '''


class ProductReviewAdminForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = models.ProductReview
        fields = '__all__'


class ProductReviewAdminAbstract(abstracts.ModelAdminAbstract):
    form = ProductReviewAdminForm
    list_display = ['product', 'rating', 'comment', 'is_approved', ]
    list_filter = ['product', 'rating', 'is_approved', ]


class ShopReviewAdminForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea())

    class Meta:
        model = models.ShopReview
        fields = '__all__'


class ShopReviewAdminAbstract(abstracts.ModelAdminAbstract):
    form = ShopReviewAdminForm
    list_display = ['shop', 'rating', 'comment', 'is_approved', ]
    list_filter = ['shop', 'rating', 'is_approved', ]


''' Registration of Admin models '''

admin.site.register(models.Currency)
admin.site.register(models.Manufacturer)
admin.site.register(models.Category)
admin.site.register(models.AttributeGroup)
admin.site.register(models.Attribute)
admin.site.register(models.Product, ProductAdminAbstract)
admin.site.register(models.Shop, ShopAdminAbstract)
admin.site.register(models.ShopProduct, ShopProductAdminAbstract)

admin.site.register(models.ProductReview, ProductReviewAdminAbstract)
admin.site.register(models.ShopReview, ShopReviewAdminAbstract)

