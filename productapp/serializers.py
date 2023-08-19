from rest_framework import serializers
from .models import Category, Product, SaleProduct


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name')


class ProductSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    updated = serializers.ReadOnlyField()
    regular_price = serializers.ReadOnlyField(source='product_price')
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    @staticmethod
    def get_discounted_price(obj):
        sale_product = SaleProduct.objects.filter(product=obj).first()
        if sale_product and sale_product.sale:
            sale_percentage = sale_product.sale_percentage
            return obj.product_price * (1 - sale_percentage / 100)
        return None


class SaleProductSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    updated = serializers.ReadOnlyField()

    class Meta:
        model = SaleProduct
        fields = ('category', 'product', 'sale')