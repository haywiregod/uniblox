from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/v1/",
        include(
            [
                path("user/", include("user.urls")),
                path("cart/", include("cart.urls")),
                path("backoffice/", include("backoffice.urls")),
            ]
        ),
    ),
]
