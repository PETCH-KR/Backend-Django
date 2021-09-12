import json
import os
import jwt
import requests
import random

from bson import ObjectId
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from server.serializers import UserSerializer, ChangePasswordSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from server.models import User
from server.utils.jwt import generate_refresh_token, generate_access_token
from server.utils import error_collection, success_util


class SignupView(APIView):
    @swagger_auto_schema(
        security=[],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="비밀번호"
                ),
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="닉네임"),
            },
        ),
        responses={
            201: success_util.SUCCESS_SIGNUP.as_obj(),
            400: error_collection.SIGNUP_400_EMAIL_ALREADY_EXIST.as_md()
            + error_collection.SIGNUP_400_NAME_ALREADY_EXIST.as_md()
            + error_collection.SIGNUP_400_NULL_EMAIL_PASSWORD.as_md(),
        },
    )
    def post(self, request):
        if (
            not request.data.get("password")
            or not request.data.get("email")
            or not request.data.get("name")
        ):
            response_object = {
                "success": False,
                "message": "이메일,비밀번호 또는 닉네임을 입력해주세요.",
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
            elif serializer.errors["name"]:
                response_object = {
                    "success": False,
                    "message": "이미 사용중인 닉네임입니다.",
                    "code": "SIGNUP_400_NAME_ALREADY_EXIST",
                }
                return Response(response_object, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    methods=["POST"],
    security=[],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
        },
    ),
    responses={
        200: success_util.SUCCESS_VERIFY_EMAIL.as_obj(),
        400: error_collection.SIGNUP_400_NULL_EMAIL.as_md(),
    },
)
@api_view(["POST"])
def verify_email(request):
    email = request.data.get("email")
    if not email:
        return Response(
            {
                "success": False,
                "message": "이메일을 입력해주세요.",
                "code": "SIGNUP_400_NULL_EMAIL",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
    ex_user = User.objects.filter(email=email)
    if len(ex_user) == 0:
        return Response(
            {"success": True, "message": "사용 가능한 이메일입니다.", "data": {"email": email}},
        )
    else:
        return Response(
            {
                "success": False,
                "code": "SIGNUP_400_EMAIL_ALREADY_EXIST",
                "message": "이미 사용중인 이메일입니다.",
            },
            status=status.HTTP_400_BAD_REQUEST,
        )


@swagger_auto_schema(
    methods=["POST"],
    security=[],
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
    security=[],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "token": openapi.Schema(type=openapi.TYPE_STRING, description="카카오 액세스 토큰"),
        },
    ),
    responses={
        200: success_util.SUCCESS_KAKAO.as_obj(),
        400: error_collection.KAKAO_400_NOT_FOUND_TOKEN.as_md(),
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
                "code": "KAKAO_400_NOT_FOUND_TOKEN",
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
    security=[],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "token": openapi.Schema(type=openapi.IN_HEADER, description="리프레시 토큰"),
        },
    ),
    responses={
        200: success_util.SUCCESS_REFRESH_TOKEN.as_obj(),
        403: error_collection.JWT_403_NOT_FOUND_REFRESHTOKEN.as_md()
        + error_collection.JWT_403_EXPIRED_REFRESHTOKEN.as_md(),
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
                    "code": "JWT_403_NOT_FOUND_REFRESHTOKEN",
                },
                status=status.HTTP_403_FORBIDDEN,
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
                "code": "JWT_403_EXPIRED_REFRESHTOKEN",
            },
            status=status.HTTP_403_FORBIDDEN,
        )


@swagger_auto_schema(
    methods=["POST"],
    security=[],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(
                type=openapi.TYPE_STRING, description="인증번호 받을 이메일"
            ),
        },
    ),
    responses={
        200: success_util.SUCCESS_SEND_RESET_EMAIL.as_obj(),
    },
)
@api_view(["POST"])
def send_reset_password_email(request):
    reciever = request.data.get("email")
    verified_number = random.randrange(100000, 999999)
    requests.post(
        "https://api.mailgun.net/v3/ziho-dev.com/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": "cau.capstone10@gmail.com",
            "to": reciever,
            "subject": "[Petch] 비밀번호 찾기 인증번호 안내",
            "template": "petch-password",
            "h:X-Mailgun-Variables": json.dumps({"verified_number": verified_number}),
        },
    )
    return Response(
        {
            "success": True,
            "message": "비밀번호 찾기 메일이 전송되었습니다.",
            "data": {
                "verified_number": verified_number,
            },
        }
    )


@swagger_auto_schema(
    methods=["POST"],
    security=[],
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
            "new_password": openapi.Schema(
                type=openapi.TYPE_STRING, description="변경할 비밀번호"
            ),
        },
    ),
    responses={
        200: success_util.SUCCESS_RESET_PASSWORD.as_obj(),
    },
)
@api_view(["POST"])
def reset_user_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        email = request.data.get("email")
        user = User.objects.get(email=email)
        user.set_password(request.data.get("new_password"))
        user.save()
        response = {
            "success": True,
            "message": "비밀번호가 성공적으로 변경되었습니다.",
            "data": {"email": email},
        }

        return Response(response)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
