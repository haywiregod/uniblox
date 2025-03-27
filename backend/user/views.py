from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from user.models import PlatformUser
from rest_framework.authtoken.models import Token
from django.db import transaction


class UserViewSet(ViewSet):

    def get_authenticators(self):
        action_map = {key.lower(): value for key, value in self.action_map.items()}
        action_name = action_map.get(self.request.method.lower())
        if action_name in ["login"]:
            return []
        return super().get_authenticators()

    @transaction.atomic
    def login(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        if not email or not password:
            return Response({"error": "Email and password are required."}, status=400)
        user = PlatformUser.objects.filter(email=email).first()
        if not user or not user.check_password(password):
            return Response({"error": "Invalid email or password."}, status=401)

        Token.objects.filter(user=user).delete()

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key})

    @transaction.atomic
    def signup(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)
        if not email or not password:
            return Response({"error": "Email and password are required."}, status=400)
        user = PlatformUser.objects.filter(email=email).exists()
        if user:
            return Response({"error": "User already exists."}, status=400)
        user = PlatformUser.objects.create_user(email=email, password=password)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})
