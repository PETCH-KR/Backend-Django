from rest_framework import serializers
from server.models import Airport


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        # fields = "__all__"
        fields = ["name", "IATA", "country"]
