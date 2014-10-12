from django.contrib import admin
from core import models as core_models
import models


class ProductAdmin(core_models.ModelAdmin):
    pass


admin.site.register(models.Currency)
admin.site.register(models.Manufacturer)
admin.site.register(models.Category)
admin.site.register(models.AttributeGroup)
admin.site.register(models.Attribute)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductReview)
admin.site.register(models.Shop)
admin.site.register(models.ShopReview)
admin.site.register(models.ShopProductPrice)

