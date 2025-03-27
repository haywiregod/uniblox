from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from user.models import PlatformUser
from cart.models import Cart, Product, CartItem
from order.models import Order, OrderItems, Coupon
from .serializers import CartSerializer
from django.db import transaction
from django.conf import settings


class CartViewset(ViewSet):

    def get(self, request):
        user: PlatformUser = request.user
        cart: Cart = user.cart
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    @transaction.atomic
    def add_product(self, request, product_id):
        user: PlatformUser = request.user
        cart: Cart = user.cart
        try:
            product: Product = Product.objects.get(
                id=product_id, available_quantity__gt=0
            )
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=404)
        cart_items = cart.items.all()

        if cart_items.filter(product=product).exists():
            cart_item: CartItem = cart_items.get(product=product)
            if cart_item.quantity >= product.available_quantity:
                return Response({"error": "Maximum quantity reached."}, status=400)
            cart_item.quantity += 1
            cart_item.save()
        else:
            cart.items.create(product=product, quantity=1)

        return Response()

    @transaction.atomic
    def remove_product(self, request, product_id):
        user: PlatformUser = request.user
        cart: Cart = user.cart
        cart.items.filter(product__id=product_id).delete()
        return Response()

    @transaction.atomic
    def check_out(self, request):
        user: PlatformUser = request.user
        cart: Cart = user.cart

        if not cart.items.exists():
            return Response({"error": "Cart is empty."}, status=400)

        coupon = request.data.get("coupon", None)
        if coupon:
            coupon = Coupon.objects.filter(code__iexact=coupon, is_active=True)
            if not coupon.exists():
                return Response({"error": "Invalid coupon code."}, status=400)
            coupon = coupon.first()

            # validate coupon
            total_orders_yet = (
                Order.objects.filter(status=Order.Status.PLACED).count() + 1
            )
            is_valid = (
                total_orders_yet > settings.NTH_ORDER_FOR_COUPON
                and total_orders_yet % settings.NTH_ORDER_FOR_COUPON == 0
            )
            if not is_valid:
                return Response(
                    {"error": "Coupon is not valid for this order."}, status=400
                )
        if coupon:
            applicable_discount = coupon.discount
        else:
            applicable_discount = 0

        order_value = 0
        order = Order.objects.create(
            user=user, applied_coupon=coupon, value=order_value, final_value=order_value
        )
        for item in cart.items.all():
            item: CartItem
            order_value += item.product.price * item.quantity
            OrderItems.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                mrp=item.product.price,
            )

        final_value = order_value - (order_value * applicable_discount / 100)
        order.value = order_value
        order.final_value = final_value
        order.status = Order.Status.PLACED
        order.save()
        if coupon:
            coupon.is_active = False
            coupon.save()

        cart.items.all().delete()
        return Response()
