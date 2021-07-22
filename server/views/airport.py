from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from server.models.airport import Airport
from server.serializers.airport import *
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import (
    SessionAuthentication,
    BasicAuthentication,
    TokenAuthentication,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets
from django.shortcuts import get_object_or_404


class AirportViewSet(viewsets.ModelViewSet):
    lookup_field = "IATA"
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()


class AirportGenericAPIView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = AirportSerializer
    queryset = Airport.objects.all()

    lookup_field = "id"  # add keyword argument

    # authentication_classes = [SessionAuthentication, BasicAuthentication]  # check session first, then basic
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, IATA):
        if IATA:
            return self.retrieve(request)
        else:
            return self.list(request)  # ListModelMixin will handle

    def post(self, request):
        return self.create(request)  # CreateModelMixin will handle

    def put(self, request, id=None):
        return self.update(request, id)  # UpdateModelMixin will handle

    def delete(self, request, id):
        return self.destroy(request, id)
