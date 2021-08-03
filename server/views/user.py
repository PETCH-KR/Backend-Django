import os
import jwt
import requests
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from server.serializers import UserSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from server.models import User
from server.utils.jwt import generate_refresh_token, generate_access_token
from server.utils import error_collection, success_util


class SignupView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="비밀번호"
                ),
            },
        ),
        responses={
            201: success_util.SUCCESS_SIGNUP.as_obj(),
            400: error_collection.SIGNUP_400_EMAIL_ALREADY_EXIST.as_md()
            + error_collection.SIGNUP_400_NULL_EMAIL_PASSWORD.as_md(),
        },
    )
    def post(self, request):
        if not request.data.get("password") or not request.data.get("email"):
            response_object = {
                "success": False,
                "message": "이메일 또는 비밀번호를 입력해주세요.",
                "code": "SIGNUP_400_NULL_EMAIL_PASSWORD",
            }
            return Response(response_object, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            response_object = {
                "success": True,
                "message": "성공적으로 회원가입이 완료되었습니다.",
                "data": {"user": UserSerializer(new_user).data},
            }
            return Response(response_object, status=status.HTTP_201_CREATED)
        else:
            if serializer.errors["email"]:
                response_object = {
                    "success": False,
                    "message": "이미 사용중인 이메일입니다.",
                    "code": "SIGNUP_400_EMAIL_ALREADY_EXIST",
                }
                return Response(response_object, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    methods=["POST"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
            "password": openapi.Schema(type=openapi.TYPE_STRING, description="비밀번호"),
        },
    ),
    responses={
        200: success_util.SUCCESS_SIGNIN.as_obj(),
        400: error_collection.SIGNIN_400_NULL_EMAIL_PASSWORD.as_md(),
        401: error_collection.SIGNIN_401_INVALID_EMAIL_PASSWORD.as_md(),
    },
)
@api_view(["POST"])
def signin(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if not email or not password:
        return Response(
            {
                "success": False,
                "message": "이메일 또는 비밀번호를 입력해주세요.",
                "code": "SIGNIN_400_NULL_EMAIL_PASSWORD",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    user = authenticate(email=email, password=password)
    if user is not None:
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)
        return Response(
            {
                "success": True,
                "message": "로그인에 성공했습니다.",
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "email": user.email,
                },
            },
            status=status.HTTP_200_OK,
        )
    else:
        return Response(
            {
                "success": False,
                "code": "SIGNIN_401_INVALID_EMAIL_PASSWORD",
                "message": "이메일 또는 비밀번호를 확인해주세요.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


@swagger_auto_schema(
    methods=["POST"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "token": openapi.Schema(type=openapi.TYPE_STRING, description="카카오 액세스 토큰"),
        },
    ),
    responses={
        200: success_util.SUCCESS_KAKAO.as_obj(),
        400: error_collection.KAKAO_400_NULL_TOKEN.as_md(),
    },
)
@api_view(["POST"])
def kakao(request):
    token = request.data.get("token")
    if not token:
        return Response(
            {
                "success": False,
                "message": "카카오로부터 받은 토큰을 보내주세요.",
                "code": "KAKAO_400_NULL_TOKEN",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    profile_request = requests.get(
        "https://kapi.kakao.com/v2/user/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    profile_json = profile_request.json()
    kakao_account = profile_json.get("kakao_account")
    email = kakao_account.get("email", None)
    if not User.objects.filter(provider="KAKAO", email=email).exists():
        User(
            provider="KAKAO",
            email=email,
        ).save()
    user = User.objects.get(provider="KAKAO", email=email)
    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)
    return Response(
        {
            "success": True,
            "message": "카카오 로그인에 성공했습니다.",
            "data": {
                "access_token": access_token,
                "refresh_token": refresh_token,
                "email": user.email,
            },
        }
    )


@swagger_auto_schema(
    methods=["POST"],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "token": openapi.Schema(type=openapi.TYPE_STRING, description="카카오 액세스 토큰"),
        },
    ),
    responses={
        200: success_util.SUCCESS_REFRESH_TOKEN.as_obj(),
        400: error_collection.JWT_400_NULL_TOKEN.as_md(),
        401: error_collection.JWT_401_TOKEN_EXPIRED.as_md(),
    },
)
@api_view(["POST"])
def refresh(request):
    try:
        refresh_token = request.headers.get("refreshtoken")
        if refresh_token is None:
            return Response(
                {
                    "success": False,
                    "message": "refresh_token을 보내주세요.",
                    "code": "JWT_400_NULL_TOKEN",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        decoded = jwt.decode(
            refresh_token, os.getenv("REFRESH_SECRET_KEY"), algorithms=["HS256"]
        )
        id = decoded.get("id")
        user = User.objects.get(id=id)
        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        return Response(
            {
                "success": True,
                "message": "access_token이 재발급되었습니다.",
                "data": {
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "email": user.email,
                },
            }
        )
    except jwt.ExpiredSignatureError:
        return Response(
            {
                "success": False,
                "message": "refresh_token이 만료되었습니다.",
                "code": "JWT_401_TOKEN_EXPIRED",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
