from django.db import models
from user.models import PlatformUser
from product.models import Product
from django.conf import settings
import random
import string


class Coupon(models.Model):
    code = models.CharField(max_length=10)
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    is_active = models.BooleanField(default=True)


class Order(models.Model):
    class Status:
        PENDING = "PENDING"
        PLACED = "PLACED"
        COMPLETED = "COMPLETED"
        CANCELLED = "CANCELLED"

    STAUS_CHOICES = (
        (Status.PENDING, "PENDING"),
        (Status.PLACED, "PLACED"),
        (Status.COMPLETED, "COMPLETED"),
        (Status.CANCELLED, "CANCELLED"),
    )

    user = models.ForeignKey(PlatformUser, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STAUS_CHOICES, default=Status.PENDING
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)
    final_value = models.DecimalField(max_digits=10, decimal_places=2)
    applied_coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    mrp = models.DecimalField(max_digits=10, decimal_places=2)


def on_order_save(sender, instance, **kwargs):
    if instance.status == Order.Status.PLACED:
        # create a coupon
        total_orders_yet = Order.objects.filter(status=Order.Status.PLACED).count()
        if total_orders_yet < settings.NTH_ORDER_FOR_COUPON:
            return
        generate_coupon = total_orders_yet % settings.NTH_ORDER_FOR_COUPON == 0
        if generate_coupon:
            # deactivate other coupons
            Coupon.objects.filter(is_active=True).update(is_active=False)
            code = "".join(random.choices(string.ascii_uppercase + string.digits, k=7))
            Coupon.objects.create(
                code=code,
                discount=settings.COUPON_DISCOUNT_PERCENTAGE,
            )


models.signals.post_save.connect(on_order_save, sender=Order)
