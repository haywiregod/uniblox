from django.urls import path, include
from .views import UserViewSet

urlpatterns = [path("login/", UserViewSet.as_view({"post": "login"}))]
