from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from server.serializers import UserSerializer
from server.models import User


class UserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            new_user = serializer.save()
            response_object = {
                "success": True,
                "message": "성공적으로 회원가입이 완료되었습니다.",
                "data": {"user": UserSerializer(new_user).data},
            }

            return Response(response_object)
        else:
            response_object = {
                "success": False,
                "message": "에러 발생",
                "data": {"error": serializer.errors},
            }
            return Response(response_object, status=status.HTTP_400_BAD_REQUEST)
