from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from order.models import Order, OrderItems, Coupon
from django.db import transaction
from django.conf import settings
from django.db.models import Sum, F, Value, DecimalField, IntegerField
from django.db.models.functions import Coalesce
import random
import string


class BackOfficeViewset(ViewSet):
    @transaction.atomic
    def generate_coupons(self, request):
        # if not request.user.is_staff:
        #     return Response({"error": "Unauthorized"}, status=401)
        total_orders_yet = Order.objects.filter(status=Order.Status.PLACED).count()
        num_coupons_to_generate = request.data.get("num_coupons", 1)
        generate_coupon = total_orders_yet % settings.NTH_ORDER_FOR_COUPON == 0
        if generate_coupon:
            # deactivate other coupons
            coupons_to_create = []
            for i in range(num_coupons_to_generate):
                # genrate a random string of 7 Characters
                code = "".join(
                    random.choices(string.ascii_uppercase + string.digits, k=7)
                )
                coupon = Coupon(
                    code=code,
                    discount=settings.COUPON_DISCOUNT_PERCENTAGE,
                )
                coupons_to_create.append(coupon)

            Coupon.objects.bulk_create(coupons_to_create)
            return Response(
                Coupon.objects.filter(
                    id__in=[coupon.id for coupon in coupons_to_create]
                ).values_list("code", flat=True)
            )
        else:
            return Response(
                {
                    "error": f"Cannot generate coupons because total orders yet is not a multiple of {settings.NTH_ORDER_FOR_COUPON}"
                },
                status=400,
            )

    def get_stats(self, request):
        # if not request.user.is_staff:
        #     return Response({"error": "Unauthorized"}, status=401)

        product_summary = (
            OrderItems.objects.filter(order__status=Order.Status.PLACED)
            .select_related("order", "product")
            .values("product__id", "product__name")
            .annotate(
                total_quantity=Sum("quantity", output_field=IntegerField()),
                total_purchase_amount=Sum(
                    F("quantity") * F("mrp"), output_field=DecimalField()
                ),
            )
        )

        # Query to get all applied coupons and total discount amount
        coupon_summary = (
            Order.objects.filter(
                applied_coupon__isnull=False, status=Order.Status.PLACED
            )
            .values("applied_coupon__code")
            .annotate(
                total_discount_amount=Sum(
                    F("value") - F("final_value"), output_field=DecimalField()
                ),
                usage_count=Sum(Value(1)),
            )
        )

        total_discount = Order.objects.filter(
            applied_coupon__isnull=False, status=Order.Status.PLACED
        ).aggregate(
            total_discount=Coalesce(
                Sum(F("value") - F("final_value"), output_field=DecimalField()),
                0,
                output_field=DecimalField(),
            )
        )[
            "total_discount"
        ]

        results = {
            "product_summary": list(product_summary),
            "coupon_summary": list(coupon_summary),
            "total_discount_amount": total_discount,
        }

        return Response(results)
