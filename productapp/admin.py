from django.contrib import admin
from .models import Category, Product, SaleProduct


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'product_name', 'product_price', 'created', 'updated')
    list_filter = ('product_name', 'available', 'created')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(available=True)


@admin.register(SaleProduct)
class SaleProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'sale', 'created', 'updated')

