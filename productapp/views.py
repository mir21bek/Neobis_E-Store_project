from rest_framework.response import Response

from .serializers import CategorySerializer, ProductSerializer, SaleProductSerializer
from rest_framework import generics
from .models import Product, Category, SaleProduct
from rest_framework import permissions
from paginations import ProductPagination


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.AllowAny]


class ProductCreateUpdateApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser]

    def perform_update(self, serializer):
        instance = serializer.save()
        sale_product = SaleProduct.objects.filter(product=instance).first()

        if sale_product and sale_product.sale:
            sale_percentage = sale_product.sale_percentage
            discounted_price = instance.product_price * (1 - sale_percentage / 100)
            instance.product_price = discounted_price
            instance.save()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        sale_product = SaleProduct.objects.filter(product=instance).first()

        if sale_product and sale_product.sale:
            sale_percentage = sale_product.sale_percentage
            request.data['product_price'] = instance.product_price * (1 - sale_percentage / 100)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class SaleProductApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SaleProduct.oblects.all()
    serializer_class = SaleProductSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAdminUser]
