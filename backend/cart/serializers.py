from rest_framework import serializers
from product.serializers import ProductSerializer
from cart.models import Cart, CartItem
from order.models import Order, Coupon


class CartItemSerializer(serializers.ModelSerializer):

    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ("product", "quantity")


class CartSerializer(serializers.ModelSerializer):

    items = CartItemSerializer(many=True)

    applicable_coupons = serializers.SerializerMethodField("get_applicable_coupons")

    def get_applicable_coupons(self, obj):
        return Coupon.objects.filter(is_active=True).values_list("code", flat=True)

    class Meta:
        model = Cart
        exclude = ("id", "user")
