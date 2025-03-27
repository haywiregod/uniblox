from datetime import datetime, timedelta
import logging
from rest_framework import exceptions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.request import Request
from django.conf import settings
from user.models import PlatformUser
from django.db.models import Q
from django.utils import timezone

logger = logging.getLogger(__name__)


class ExpiringTokenAuthentication(TokenAuthentication):
    def authenticate(self, request):
        # get token_key from request headers Authorization as "Bearer <token_key>"
        if "Authorization" not in request.headers:
            raise exceptions.AuthenticationFailed("Authorization header is missing")

        auth_header = request.headers["Authorization"]
        if not auth_header.startswith("Bearer "):
            raise exceptions.AuthenticationFailed("Invalid Authorization header")

        token_key = auth_header.split(" ")[1]

        try:
            token = Token.objects.prefetch_related("user").get(key=token_key)
        except Token.DoesNotExist:
            raise exceptions.AuthenticationFailed("Invalid token")

        if is_token_expired(token):
            raise exceptions.AuthenticationFailed("Token has expired")

        user = token.user

        return (user, token)


def is_token_expired(token: Token):
    current_time_utc = timezone.now()
    return token.created < current_time_utc - timedelta(
        hours=settings.TOKEN_EXPIRE_HOURS
    )
