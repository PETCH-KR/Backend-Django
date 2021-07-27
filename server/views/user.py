from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from server.serializers import UserSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


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
