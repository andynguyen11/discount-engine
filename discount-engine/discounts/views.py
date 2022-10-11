from datetime import date

from .models import Discount
from .serializers import DiscountSerializer, CartSerializer

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


def apply_discount(discount, cart):
    if discount.type == 'percent':
        return discount.percent.apply(cart)
    elif discount.type == 'fixed':
        return discount.fixed.apply(cart)
    elif discount.type == 'product':
        return discount.product.apply(cart)
    return cart


class DiscountViewSet(APIView):
    queryset = Discount.objects.all()
    serializer_class = CartSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        cart = serializer.validated_data
        code = cart['discount_code'].upper() if cart['discount_code'] else False
        greatest_discount = 0

        if code:
            discount = Discount.objects.get(code=code)
            discount_total = apply_discount(discount, cart)
            greatest_discount = discount_total if discount_total > greatest_discount else greatest_discount
        else:
            promos = Discount.objects.filter(active=True, start_date__lte=date.today(), end_date__gte=date.today())
            for promo in promos:
                discount_total = apply_discount(promo, cart)
                greatest_discount = discount_total if discount_total > greatest_discount else greatest_discount

        cart['discount_total'] = greatest_discount
        cart['subtotal'] = float(cart['subtotal']) - float(cart['discount_total'])

        return Response(cart, status=status.HTTP_200_OK)