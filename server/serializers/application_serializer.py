from rest_framework import serializers
from server.models import Dog


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dog
        fields = "__all__"
