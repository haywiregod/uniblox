from django.db import models
from user.models import PlatformUser
from product.models import Product


class Cart(models.Model):
    user = models.OneToOneField(
        PlatformUser, on_delete=models.CASCADE, related_name="cart"
    )


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
