from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product, SaleProduct


class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'parent',)
    list_filter = ('parent',)
    search_fields = ('name',)


admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_price', 'discounted_price', 'available')
    list_filter = ('available', 'created', 'category')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(available=True)


admin.site.register(Product, ProductAdmin)


@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'sale', 'created', 'updated')
