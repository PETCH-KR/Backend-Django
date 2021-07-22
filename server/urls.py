from django.urls import path, include
from rest_framework.generics import GenericAPIView
from server.views import AirportViewSet, AirportGenericAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("airport", AirportViewSet, basename="airport")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "generic",
        GenericAPIView.as_view(),
    ),
]
