import os
import jwt
from rest_framework import exceptions
from rest_framework import authentication
from server.models import User, Organization
from bson import ObjectId


class JWTAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        try:
            token = request.headers.get("AUTHORIZATION")
            if token is None:
                return None
            token_type, jwt_token = token.split(" ")
            decoded = jwt.decode(
                jwt_token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"]
            )
            id = decoded.get("id")
            if token_type == "Bearer":
                user = User.objects.get(_id=ObjectId(id))
            else:
                user = Organization.objects.get(_id=ObjectId(id))
            return (user, None)
        except jwt.exceptions.DecodeError:
            raise exceptions.AuthenticationFailed(
                {
                    "success": False,
                    "message": "잘못된 토큰입니다.",
                    "code": "JWT_403_INVALID_ACCESSTOKEN",
                }
            )
        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed(
                {
                    "success": False,
                    "message": "토큰이 만료되었습니다.",
                    "code": "JWT_403_EXPIRED_ACCESSTOKEN",
                }
            )
