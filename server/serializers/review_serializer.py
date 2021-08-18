from rest_framework import serializers
from server.models import UserReview, OrganizationReview
from server.serializers import *


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        fields = "__all__"


class OrganizationReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganizationReview
        fields = "__all__"
