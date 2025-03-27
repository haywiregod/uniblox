from django.urls import path, include
from .views import CartViewset

urlpatterns = [
    path("", CartViewset.as_view({"get": "get"})),
    path(
        "product/<int:product_id>/",
        CartViewset.as_view({"post": "add_product", "delete": "remove_product"}),
    ),
    path("checkout/", CartViewset.as_view({"post": "check_out"})),
]
