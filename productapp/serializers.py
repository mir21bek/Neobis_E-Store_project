from rest_framework import serializers
from .models import Category, Product, SaleProduct, Rating, Comment
from .utils import calculate_discounted_price


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'parent')


class ProductSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    updated = serializers.ReadOnlyField()
    regular_price = serializers.ReadOnlyField(source='product_price')
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ('category', 'id', 'product_name', 'product_description',
                  'product_image', 'available', 'created', 'updated', 'regular_price',
                  'discounted_price')

    @staticmethod
    def get_discounted_price(obj):
        sale_product = SaleProduct.objects.filter(product=obj).first()
        if sale_product and sale_product.sale:
            sale_percentage = sale_product.sale_percentage
            return calculate_discounted_price(obj.product_price, sale_percentage)
        return None


class SaleProductSerializer(serializers.ModelSerializer):
    created = serializers.ReadOnlyField()
    updated = serializers.ReadOnlyField()

    class Meta:
        model = SaleProduct
        fields = ('category', 'product', 'sale', 'sale_percentage', 'created', 'updated')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('user', 'product', 'rating')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('user', 'product', 'rating', 'text', 'created')
