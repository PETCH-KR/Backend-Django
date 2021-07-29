from server.models.airport import Airport
from server.serializers.airport import *
from rest_framework.response import Response
from rest_framework.views import APIView


class AirportAPIView(APIView):
    def get_object(self, name):
        queryset = Airport.objects.all()

        name_match = queryset.filter(name__contains=name)
        country_match = queryset.filter(country__contains=name)
        IATA_match = queryset.filter(IATA__contains=name)
        result = name_match | country_match | IATA_match

        return result

    def get(self, request, name):
        airport = self.get_object(name)
        serializer = AirportSerializer(airport, many=True)
        airports_data = serializer.data
        airports_len = len(airports_data)
        response_object = {
            "success": True,
            "message": f"{airports_len}개의 공항 검색 결과가 나왔습니다.",
            "data": {"airports_data": airports_data},
        }
        return Response(response_object)
