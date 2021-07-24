from django.urls import path
from server.views import AirportAPIView, UserView


urlpatterns = [
    path("", UserView.as_view()),
    path("airport/<str:name>/", AirportAPIView.as_view()),
]
