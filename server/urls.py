from django.urls import path
from server.views import AirportAPIView, SignupView


urlpatterns = [
    path("user/signup", SignupView.as_view()),
    path("airport/<str:name>/", AirportAPIView.as_view()),
]
