from server.serializers.dog_serializer import DogSerializer
from rest_framework import serializers
from server.models import Application
from server.serializers import *


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = "__all__"
