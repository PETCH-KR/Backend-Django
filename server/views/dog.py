from server.models.dog_model import Dog
from server.serializers.dog_serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from bson import ObjectId
from server.utils.upload import upload_image



class DogAPIView(APIView):
    def post_image(self, request):
        image = request.FILES["image"]
        try:
            public_uri = upload_image(image, "dog")
            return public_uri
        except:
            return False

    def post(self, request):
        data = request.data
        assert request.FILES["image"]

        image_save = self.post_image(request)

        assert image_save

        data["image"] = image_save

        serializer = DogInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "저장완료", "data": data})
        else:
            return Response({"success": False, "message": "저장실패", "data": data})


class DogDetailAPIView(APIView):
    def post_image(self, request):
        image = request.FILES["image"]
        try:
            public_uri = upload_image(image, "dog")
            return public_uri
        except:
            return False

    def get_object(self, _id):
        try:
            return Dog.objects.get(_id=ObjectId(_id))
        except Dog.DoesNotExist:
            return False

    def put(self, request, _id):
        Dog = self.get_object(_id)
        assert Dog
        assert request.FILES["image"]

        image_save = self.post_image(request)
        print("\n\n\n", image_save, "\n\n\n")

        assert image_save

        data = request.data
        data["image"] = image_save

        print("\n\n\n", data, "\n\n\n")

        serializer = DogSerializer(Dog, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "수정완료", "data": data})
        else:
            return Response({"success": False, "message": "수정실패", "data": data})

    def delete(self, request, _id):
        Dog = self.get_object(_id)
        assert Dog

        Dog.delete()
        return Response({"success": True, "message": "삭제완료"})


class DogBasicAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get_queryset(self, request):
        queryset = Dog.objects.all()
        destination = request.GET["dst"]
        match = queryset.filter(destination__contains=destination)
        return match

    def get(self, request):
        dog = self.get_queryset(request)
        serializer = DogBasicSerializer(dog, many=True)
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

        match = Dog.objects.get(_id=_id)
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


class DogInfoAPIView(APIView):
    def get_queryset(self, request):
        n = int(request.GET["number"])
        match = Dog.objects.order_by("deadline", "name")[:n]
        print(match)
        return match

    def get(self, request):
        dog = self.get_queryset(request)
        serializer = DogInfoSerializer(dog, many=True)
        dogs_data = serializer.data
        dogs_len = len(dogs_data)
        response_object = {
            "success": True,
            "message": f"{dogs_len}개의 유기견 검색 결과가 나왔습니다.",
            "data": {"dogs_data": dogs_data},
        }
        return Response(response_object)


class DogSearchAPIView(APIView):
    # permission_classes = [IsAuthenticated]
    def get_queryset(self, request):
        queryset = Dog.objects.all()
        dst = request.GET["dst"]
        date = request.GET["date"]
        match = queryset.filter(destination=dst).exclude(deadline__gt=date)
        return match

    def get(self, request):
        dog = self.get_queryset(request)
        serializer = DogBasicSerializer(dog, many=True)
        dogs_data = serializer.data
        dogs_len = len(dogs_data)
        response_object = {
            "success": True,
            "message": f"{dogs_len}개의 유기견 검색 결과가 나왔습니다.",
            "data": {"dogs_data": dogs_data},
        }
        return Response(response_object)
