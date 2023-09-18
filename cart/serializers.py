from rest_framework import serializers


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartAddProductSerializer(serializers.ModelSerializer):
    quantity = serializers.ChoiceField(choices=PRODUCT_QUANTITY_CHOICES)
    override = serializers.BooleanField(required=False, initial=False)
