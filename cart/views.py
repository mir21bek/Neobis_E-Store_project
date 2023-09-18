from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from productapp.models import Product
from .cart import Cart
from .serializers import CartAddProductSerializer


class CartViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def cart_add(self, request, *args, **kwargs):
        cart = Cart(request)
        serializer = CartAddProductSerializer(data=request.data)

        if serializer.is_valid():
            product_id = request.data.get('product_id')
            product = get_object_or_404(Product, id=product_id)
            quantity = serializer.validated_data['quantity']
            override = serializer.validated_data.get('override', False)
            cart.add(product=product, quantity=quantity, override=override)
            return Response({'message': 'Product added to cart'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
