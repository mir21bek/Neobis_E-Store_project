from rest_framework.response import Response

from .serializers import CategorySerializer, ProductSerializer, SaleProductSerializer
from rest_framework import generics
from .models import Product, Category, SaleProduct
from rest_framework import permissions
from .paginations import ProductPagination
from .utils import calculate_discounted_price
from .permissons import IsOwnerOrAdmin


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.AllowAny]


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductCreateUpdateApiView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAdminUser, IsOwnerOrAdmin]

    def perform_create(self, serializer):
        sale_product = SaleProduct.objects.filter(product=serializer.instance).first()
        if sale_product and sale_product.sale:
            sale_percentage = sale_product.sale_percentage
            discounted_price = calculate_discounted_price(self.request.data.get('product_price'), sale_percentage)
            serializer.validated_data['product_price'] = discounted_price
        product_price = self.request.data.get('product_price')
        serializer.save(product_price=product_price)

    @staticmethod
    def perform_update(serializer):
        instance = serializer.save()
        sale_product = SaleProduct.objects.filter(product=instance).first()

        if sale_product and sale_product.sale:
            sale_percentage = sale_product.sale_percentage
            discounted_price = calculate_discounted_price(instance.product_price, sale_percentage)
            instance.product_price = discounted_price
            instance.save()

    def update(self, request, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        sale_product = SaleProduct.objects.filter(product=instance).first()

        if sale_product and sale_product.sale:
            sale_percentage = sale_product.sale_percentage
            request.data['product_price'] = calculate_discounted_price(instance.product_price, sale_percentage)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class SaleProductApiView(generics.ListCreateAPIView):
    queryset = SaleProduct.objects.filter(sale=True)
    serializer_class = SaleProductSerializer
    pagination_class = ProductPagination
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
