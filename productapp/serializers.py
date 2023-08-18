from rest_framework import serializers
from .models import Category, Product, SaleProduct


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name')


class ProductSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    updated = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = '__all__'


class SaleProductSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    updated = serializers.ReadOnlyField()

    class Meta:
        model = SaleProduct
        fields = ('category', 'product', 'sale')
