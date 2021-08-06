from rest_framework import serializers
from server.models import Dog


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = [
            "name",
            "breed",
            "deadline",
            "destination",
        ]


class DogDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = ["description"]
