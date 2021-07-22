from django.urls import path
from server.views import AirportAPIView


urlpatterns = [
    path("airport/<str:name>/", AirportAPIView.as_view()),
]
