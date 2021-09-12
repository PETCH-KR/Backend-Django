from rest_framework import serializers
from server.models import Chatroom


class ChatroomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chatroom
        fields = "__all__"