import os
import jwt
from rest_framework import exceptions
from rest_framework import authentication
from server.models import User


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.headers.get("AUTHORIZATION")
            if token is None:
                return None
            jwt_token = token
            decoded = jwt.decode(
                jwt_token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"]
            )
            id = decoded.get("id")
            user = User.objects.get(id=id)
            return (user, None)
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed("잘못된 JWT입니다.")
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("토큰이 만료되었습니다.")
