from server.serializers.airport_serializer import *
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class AirportAPIView(APIView):
    """
    공항 검색 API
    ---
    국가 및 공항명 검색
    """

    success_field = openapi.Schema(
        "success", description="성공 여부", type=openapi.TYPE_BOOLEAN
    )
    message_field = openapi.Schema(
        "detail", description="메세지", type=openapi.TYPE_STRING
    )
    data_field = openapi.Schema("data", description="검색 결과", type=openapi.TYPE_OBJECT)
    success_resp = openapi.Schema(
        "response",
        type=openapi.TYPE_OBJECT,
        properties={
            "success": success_field,
            "message": message_field,
            "data": data_field,
        },
    )

    def get_object(self, name):
        queryset = Airport.objects.all()
        name_match = queryset.filter(name__contains=name)
        country_match = queryset.filter(country__contains=name)
        IATA_match = queryset.filter(IATA__contains=name)
        result = name_match | country_match | IATA_match

        return result

    @swagger_auto_schema(responses={200: success_resp})
    def get(self, request, name):
        airport = self.get_object(name)
        serializer = AirportSerializer(airport, many=True)
        airports_data = serializer.data
        airports_len = len(airports_data)
        return Response(
            {
                "success": True,
                "message": f"{airports_len}개의 공항 검색 결과가 나왔습니다.",
                "data": {"airports_data": airports_data},
            }
        )

