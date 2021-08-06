from server.models.dog import Dog
from server.serializers.dog import *
from rest_framework.response import Response
from rest_framework.views import APIView


class DogAPIView(APIView):
    def get_object(self, destination):
        queryset = Dog.objects.all()
        match = queryset.filter(destiniation__contains=destination)
        return match

    def get(self, request, destination):
        dog = self.get_object(destination)
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
    def get_object(self, id):
        queryset = self.objects.all()
        match = queryset.filter(id=id)
        return match

    def get(self, request, id):
        desc = self.get_object(id)
        serializer = DogDescriptionSerializer(desc)
        desc_data = serializer.data
        desc_len = len(desc_data)
        response_object = {
            "success": True,
            "message": f"{desc_len}개의 유기견 세부사항 검색 결과가 나왔습니다.",
            "data": {"dogs_data": desc_data},
        }
        return Response(response_object)
