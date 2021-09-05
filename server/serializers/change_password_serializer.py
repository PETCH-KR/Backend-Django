from rest_framework import serializers
from server.models import User


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    email = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
