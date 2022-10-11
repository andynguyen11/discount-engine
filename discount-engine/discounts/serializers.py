from rest_framework import serializers

from .models import Discount

class DiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Discount


class ProductSerializer(serializers.Serializer):
    id = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)


class CartSerializer(serializers.Serializer):
    products = serializers.ListField(
        child=ProductSerializer()
    )
    discount_code = serializers.CharField(required=False, default='')
    discount_total = serializers.DecimalField(max_digits=10, decimal_places=2, required=False, default=0.00)
    subtotal = serializers.DecimalField(max_digits=10, decimal_places=2)
