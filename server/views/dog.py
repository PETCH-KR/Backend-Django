from server.models import *
from server.serializers.dog_serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from bson import ObjectId
from server.utils.upload import upload_image
from server.utils.json_util import jsonify
from server.utils import success_util, error_collection

from django.forms.models import model_to_dict

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import status
from rest_framework.parsers import MultiPartParser


class DogAddAPIView(APIView):
    """
    Add Dog data
    """

    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post_image(self, request):
        image = request.FILES["image"]
        try:
            public_uri = upload_image(image, "dog")
            return public_uri
        except:
            return False

    @swagger_auto_schema(
        operation_description="유기견 정보 작성 API, 작성 시 header에 액세스토큰을 넣어야하고, 이름, 종, 설명, 마감 날짜, 도착지, 이미지, 기관 ID를 바디로 보내야 한다.",
        manual_parameters=[
            openapi.Parameter(
                name="accessToken",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                description="액세스토큰",
            ),
            openapi.Parameter(
                name="image",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="이미지 파일",
            ),
            openapi.Parameter(
                name="name",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="유기견 이름",
            ),
            openapi.Parameter(
                name="breed",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="유기견 견종",
            ),
            openapi.Parameter(
                name="description",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="유기견 설명",
            ),
            openapi.Parameter(
                name="deadline",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="입양 마감",
            ),
            openapi.Parameter(
                name="destination",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="도착지",
            ),
            openapi.Parameter(
                name="org_id",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="기관_id",
            ),
        ],
        responses={
            200: success_util.SUCCESS_ADD_DOG_INFO.as_obj(),
            400: error_collection.REVIEW_400_NULL_REQUEST_DATA.as_md()
            + error_collection.DOG_400_ADD_FAILED.as_md(),
        },
    )
    def post(self, request):
        data = request.data
        assert request.FILES["image"]

        image_save = self.post_image(request)

        assert image_save

        data["image"] = image_save

        org_id = request.data["org_id"]
        organization_data = Organization.objects.get(_id=ObjectId(org_id))
        organization_data = model_to_dict(organization_data)
        data["organization"] = organization_data

        serializer = DogInfoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "유기견 정보 저장 완료", "data": data})
        else:
            return Response(
                {
                    "success": False,
                    "message": "유기견 정보 저장 실패",
                    "code": "DOG_400_ADD_FAILED",
                }
            )


class DogModifyAPIView(APIView):
    """
    Modify(edit / delete) data.
    """

    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def post_image(self, request):
        image = request.FILES["image"]
        try:
            public_uri = upload_image(image, "dog")
            return public_uri
        except:
            return False

    def get_DOGobject(self, _id):
        try:
            return Dog.objects.get(_id=ObjectId(_id))
        except Dog.DoesNotExist:
            return False

    @swagger_auto_schema(
        operation_description="유기견 정보 작성 API, 작성 시 header에 액세스토큰을 넣어야하고, 이름, 종, 설명, 마감 날짜, 도착지, 이미지, 기관 ID를 바디로 보내야 한다.",
        manual_parameters=[
            openapi.Parameter(
                name="accessToken",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                description="액세스토큰",
            ),
            openapi.Parameter(
                name="image",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_FILE,
                required=True,
                description="이미지 파일",
            ),
            openapi.Parameter(
                name="name",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="유기견 이름",
            ),
            openapi.Parameter(
                name="breed",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="유기견 견종",
            ),
            openapi.Parameter(
                name="description",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="유기견 설명",
            ),
            openapi.Parameter(
                name="deadline",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="입양 마감",
            ),
            openapi.Parameter(
                name="destination",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="도착지",
            ),
            openapi.Parameter(
                name="org_id",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="기관_id",
            ),
        ],
        responses={
            200: success_util.SUCCESS_ADD_DOG_INFO.as_obj(),
            400: error_collection.REVIEW_400_NULL_REQUEST_DATA.as_md()
            + error_collection.DOG_400_MODIFY_FAILED.as_md(),
        },
    )
    def put(self, request, _id):
        Dog = self.get_object(_id)
        assert Dog
        assert request.FILES["image"]

        image_save = self.post_image(request)
        print("\n\n\n", image_save, "\n\n\n")

        assert image_save

        data = request.data
        data["image"] = image_save

        org_id = request.data["org_id"]
        organization_data = Organization.objects.get(_id=ObjectId(org_id))
        organization_data = model_to_dict(organization_data)
        data["organization"] = organization_data

        serializer = DogSerializer(Dog, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "message": "유기견 정보 수정 완료", "data": data})
        else:
            return Response(
                {
                    "success": False,
                    "message": "유기견 정보 수정 실패",
                    "code": "DOG_400_MODIFY_FAILED",
                }
            )

    @swagger_auto_schema(
        operation_description="해당 유기견의 정보를 삭제하기",
        responses={
            200: success_util.SUCCESS_DELETE_DOG_SINGLE.as_obj(),
        },
    )
    def delete(self, request, _id):
        Dog = self.get_object(_id)
        assert Dog

        Dog.delete()
        return Response({"success": True, "message": "삭제완료"})


class DogSingleAPIView(APIView):
    """
    Get single dog's data
    """

    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get_queryset(self, request):
        _id = request.GET["_id"]
        _id = ObjectId(_id)

        match = Dog.objects.get(_id=_id)
        return match

    @swagger_auto_schema(
        operation_description="해당 유기견의 정보를 불러오기",
        responses={
            200: success_util.SUCCESS_GET_DOG_SINGLE.as_obj(),
        },
    )
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


class DogDeadlineAPIView(APIView):
    """
    Sort by deadline and name
    """

    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get_queryset(self, request):
        n = int(request.GET["number"])
        match = Dog.objects.order_by("deadline", "name")[:n]
        print(match)
        return match

    @swagger_auto_schema(
        operation_description="Deadline정렬된 유기견의 정보를 불러오기",
        responses={
            200: success_util.SUCCESS_GET_DOG_DEADLINE.as_obj(),
        },
    )
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


class DogDstDateAPIView(APIView):
    """
    Search by deadline and destination
    """

    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get_queryset(self, request):
        queryset = Dog.objects.all()
        dst = request.GET["dst"]
        date = request.GET["date"]
        match = queryset.filter(destination=dst).exclude(deadline__gt=date)
        return match

    @swagger_auto_schema(
        operation_description="해당 조건에 맞는 유기견의 정보를 불러오기",
        responses={
            200: success_util.SUCCESS_GET_DOG_SEARCH.as_obj(),
        },
    )
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


######################################
# NOT CURRENTLY IN USE
######################################
class DogDstAPIView(APIView):
    """
    Search by destination.
    Not currently in use.
    """

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
