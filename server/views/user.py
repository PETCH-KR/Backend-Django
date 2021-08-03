import os
import jwt
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


class SignupView(APIView):
    success_field = openapi.Schema(
        "success", description="성공 여부", type=openapi.TYPE_BOOLEAN
    )
    message_field = openapi.Schema(
        "detail", description="메세지", type=openapi.TYPE_STRING
    )
    data_field = openapi.Schema("data", description="회원 정보", type=openapi.TYPE_OBJECT)
    success_resp = openapi.Schema(
        "response",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": success_field,
            "message": message_field,
            "data": data_field,
        },
    )
    http_method_names = ["post"]

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
        responses={201: success_resp},
    )
    def post(self, request):
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
            response_object = {
                "success": False,
                "message": "에러 발생",
                "data": {"error": serializer.errors},
            }
            return Response(response_object, status=status.HTTP_400_BAD_REQUEST)


class MeView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {
                "success": True,
                "message": "사용자 정보를 불러왔습니다.",
                "data": {"user": UserSerializer(request.user).data},
            }
        )

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def signin(request):
    email = request.data.get("email")
    password = request.data.get("password")
    if not email or not password:
        return Response(
            {
                "success": False,
                "message": "이메일 또는 비밀번호를 입력해주세요.",
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
            }
        )
    else:
        return Response(
            {
                "success": False,
                "message": "이메일 또는 비밀번호를 입력해주세요.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["POST"])
def refresh(request):
    try:
        refresh_token = request.headers.get("refreshtoken")
        if refresh_token is None:
            return Response(
                {
                    "success": False,
                    "message": "refreshtoken을 보내주세요.",
                }
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
                "message": "refreshtoken이 만료되었습니다.",
            },
            status=status.HTTP_401_UNAUTHORIZED,
        )
