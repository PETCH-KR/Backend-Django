from rest_framework import status
from rest_framework.parsers import MultiPartParser
from server.serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from bson import ObjectId
from server.utils import success_util, error_collection
from server.utils.upload import upload_image
from django.forms.models import model_to_dict
from server.utils.json_util import jsonify


class UserReviewAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser,)

    @swagger_auto_schema(
        operation_description="해당 유저 리뷰 불러오기, header에 액세스토큰을 넣어야한다.",
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
            200: success_util.SUCCESS_GET_USER_REVIEW.as_obj(),
        },
    )
    def get(self, request):
        user_id = request.user._id
        user_reviews = UserReview.objects.filter(user={"id": user_id})
        user_reviews = list(model_to_dict(review) for review in user_reviews)
        user_review_data = user_reviews
        user_review_len = len(user_review_data)
        response_object = {
            "success": True,
            "message": f"{user_review_len}개의 리뷰를 불러왔습니다.",
            "data": jsonify(user_review_data),
        }
        return Response(response_object)

    def post_image(self, request):
        image = request.FILES["image"]
        try:
            public_uri = upload_image(image, "user_review")
            return public_uri
        except:
            return False

    @swagger_auto_schema(
        operation_description="유저 리뷰 작성 API, 리뷰 시 header에 액세스토큰을 넣어야하고, 코멘트, 이미지, 기관 ID를 바디로 보내야 한다.",
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
                name="comment",
                in_=openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="리뷰 내용",
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
            200: success_util.SUCCESS_ADD_USER_REVIEW.as_obj(),
            400: error_collection.REVIEW_400_NULL_REQUEST_DATA.as_md()
            + error_collection.REVIEW_400_ADD_REVIEW_FAILED.as_md(),
        },
    )
    def post(self, request):
        user_id = request.user._id
        if not request.data.get("comment") or not request.data.get("org_id"):
            response_object = {
                "success": False,
                "message": "누락된 정보(코멘트, 기관ID)가 있습니다. 확인해주세요.",
                "code": "REVIEW_400_NULL_REQUEST_DATA",
            }
            return Response(response_object, status=status.HTTP_400_BAD_REQUEST)

        data = request.data.copy()
        data.pop("org_id")

        if request.data.get("image"):
            image_save = self.post_image(request)
            data["image"] = image_save

        user_data = User.objects.get(_id=ObjectId(user_id))
        user_data = model_to_dict(user_data)
        del user_data["password"]

        org_id = request.data["org_id"]
        organization_data = Organization.objects.get(_id=ObjectId(org_id))
        organization_data = model_to_dict(organization_data)

        data["user"] = user_data
        data["organization"] = organization_data

        serializer = UserReviewSerializer(data=data)

        if serializer.is_valid():
            new_review = serializer.save()
            return Response(
                {
                    "success": True,
                    "message": "리뷰가 성공적으로 작성되었습니다.",
                    "data": jsonify(model_to_dict(new_review)),
                }
            )
        else:
            print(serializer.errors)
            return Response(
                {
                    "success": False,
                    "message": "리뷰 저장 시 문제가 발생했습니다.",
                    "code": "REVIEW_400_ADD_REVIEW_FAILED",
                }
            )
