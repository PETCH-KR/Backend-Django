from server.models import *
from server.serializers.application_serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from bson import ObjectId
from server.utils.upload import upload_image
from server.utils.json_util import jsonify
from server.utils import success_util, error_collection

from django.forms.models import model_to_dict
from django.db.models import Prefetch

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import status
from rest_framework.parsers import MultiPartParser

import json


class ApplicationAPIView(APIView):
    """
    Add application
    """

    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get_object(self, _id):
        try:
            return Application.objects.get(_id=ObjectId(_id))
        except Application.DoesNotExist:
            return False

    @swagger_auto_schema(
        operation_description="봉사신청 등록 API, 작성 시 header에 액세스토큰을 넣어야하고, 동기, 지원서, 목적지, 출국 날짜, 도착 날짜, 강아지 ID를 바디로 보내야 한다.",
        manual_parameters=[
            openapi.Parameter(
                name="accessToken",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                description="액세스토큰",
            ),
            openapi.Parameter(
                name="motivation",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="신청 동기",
            ),
            openapi.Parameter(
                name="resume",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="지원서",
            ),
            openapi.Parameter(
                name="destination",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="목적지(IATA)",
            ),
            openapi.Parameter(
                name="departureDate",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="출국 날짜",
            ),
            openapi.Parameter(
                name="arrivalDate",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="도착 날짜",
            ),
            openapi.Parameter(
                name="dog_id",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="유기견_id",
            ),
        ],
        responses={
            200: success_util.SUCCESS_ADD_APPLICATION.as_obj(),
            400: error_collection.APPLICATION_400_NULL_REQUEST_DATA.as_md()
            + error_collection.APPLICATION_400_ADD_FAILED.as_md(),
        },
    )
    def post(self, request):
        data = request.data.copy()

        dog_id = request.data["dog"]
        dog_data = Dog.objects.get(_id=ObjectId(dog_id))
        dog_data = model_to_dict(dog_data)

        data["dog"] = dog_data
        print(data)
        serializer = ApplicationSerializer(data=data)

        if serializer.is_valid():
            new = serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "신청서 저장 완료",
                    "data": jsonify(model_to_dict(new)),
                }
            )
        else:
            print(serializer.errors)
            return Response(
                {
                    "success": False,
                    "message": "신청서 저장 실패",
                    "code": "APPLICATION_400_ADD_FAILED",
                }
            )

    @swagger_auto_schema(
        operation_description="신청서 삭제하기",
        responses={
            200: success_util.SUCCESS_DELETE_APPLICATION.as_obj(),
        },
    )
    def delete(self, request):
        _id = request.GET["_id"]
        Application = self.get_object(_id)
        if Application:
            Application.delete()
            return Response({"success": True, "message": "삭제완료"})
        else:
            return Response({"success": False, "message": "해당 신청서가 존재하지 않습니다."})

    @swagger_auto_schema(
        operation_description="해당 조건에 맞는 신청서 불러오기",
        manual_parameters=[
            openapi.Parameter(
                name="accessToken",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                description="액세스토큰",
            ),
        ],
        responses={
            200: success_util.SUCCESS_GET_APPLICATION_SEARCH.as_obj(),
        },
    )
    def get(self, request):
        desc = self.get_queryset(request)
        if not desc:
            response_object = {
                "success": False,
                "message": f"신청서 검색이 실패하였습니다.",
            }
        else:
            serializer = ApplicationSerializer(desc)
            desc_data = serializer.data

            response_object = {
                "success": True,
                "message": "세부사항 검색 결과가 나왔습니다.",
                "data": jsonify(desc_data),
            }
        return Response(response_object)


class ApplicationListAPIView(APIView):
    """
    Search by dog_id
    """

    # permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    def get_queryset(self, request):
        dog_id = request.GET["dog"]
        dog_id = ObjectId(dog_id)
        match = Application.objects.filter(dog={"_id": dog_id})
        return match

    @swagger_auto_schema(
        operation_description="해당 조건에 맞는 신청서 불러오기",
        manual_parameters=[
            openapi.Parameter(
                name="accessToken",
                in_=openapi.IN_HEADER,
                type=openapi.TYPE_STRING,
                required=True,
                description="액세스토큰",
            ),
        ],
        responses={
            200: success_util.SUCCESS_GET_APPLICATION_SEARCH.as_obj(),
        },
    )
    def get(self, request):
        app = self.get_queryset(request)
        serializer = ApplicationSerializer(app, many=True)
        application_data = serializer.data
        app_len = len(application_data)
        response_object = {
            "success": True,
            "message": f"{app_len}개의 신청서 검색 결과가 나왔습니다.",
            "data": {"dogs_data": application_data},
        }
        return Response(response_object)
