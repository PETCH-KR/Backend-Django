from rest_framework import serializers
from server.models import Dog


class DogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = [
            "_id",
            "name",
            "image",
            "breed",
            "organization",
            "deadline",
            "destination",
            "createdAt",
        ]


class DogDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = [
            "name",
            "breed",
            "organization",
            "description",
            "deadline",
            "destination",
            "createdAt",
        ]
        # fields="__all__"


class DogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = ["image", "destination"]