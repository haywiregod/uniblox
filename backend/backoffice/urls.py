from django.urls import path, include
from .views import BackOfficeViewset

urlpatterns = [
    path("generate-coupons/", BackOfficeViewset.as_view({"post": "generate_coupons"})),
    path("stats/", BackOfficeViewset.as_view({"get": "get_stats"})),
]
