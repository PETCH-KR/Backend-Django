from server.models.dog_model import Dog
from server.serializers.dog_serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from bson import ObjectId


class DogAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get_queryset(self, request):
        queryset = Dog.objects.all()
        destination = request.GET["destination"]
        match = queryset.filter(destination__contains=destination)
        print(match)
        return match

    def get(self, request):
        dog = self.get_queryset(request)
        serializer = DogSerializer(dog, many=True)
        dogs_data = serializer.data
        dogs_len = len(dogs_data)
        response_object = {
            "success": True,
            "message": f"{dogs_len}개의 유기견 검색 결과가 나왔습니다.",
            "data": {"dogs_data": dogs_data},
        }
        return Response(response_object)


class DogDescriptionAPIView(APIView):
    def get_queryset(self, request):
        _id = request.GET["_id"]
        _id = ObjectId(_id)
        match = Dog.objects.get(pk=_id)
        return match

    def get(self, request):
        desc = self.get_queryset(request)
        serializer = DogDescriptionSerializer(desc)
        desc_data = serializer.data
        desc_len = len(desc_data)
        response_object = {
            "success": True,
            "message": f"{desc_len}개의 유기견 세부사항 검색 결과가 나왔습니다.",
            "data": {"dogs_data": desc_data},
        }
        return Response(response_object)


class DogImageAPIView(APIView):
    def post(self, request):
        dog_serializer = DogImageSerializer(data=request.data)
        print(dog_serializer)
        if dog_serializer.is_valid():
            dog_serializer.save()
            return Response({"message": "success"})
        else:
            return Response({"message": "fail"})
