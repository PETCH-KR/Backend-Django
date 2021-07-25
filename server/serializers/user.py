from rest_framework import serializers
from server.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = [
            "password",
            "email",
            "phone",
            "passport",
            "provider",
        ]

    def create(self, validated_data):
        if validated_data.get("password"):
            password = validated_data.get("password")
            user = super().create(validated_data)
            user.set_password(password)
            user.save()
        # 비밀번호 필요 없는 경우, SNS 로그인
        else:
            user = super().create(validated_data)
            user.save()
        return user
