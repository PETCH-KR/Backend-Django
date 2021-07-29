from django.urls import path
from server.views import AirportAPIView, SignupView, DogAPIView, DogDescriptionAPIView

urlpatterns = [
    path("user/signup", SignupView.as_view()),
    path("airport/<str:name>/", AirportAPIView.as_view()),
    path("dog/<str:destination/", DogAPIView.as_view()),
    path("dog_description/<str:id>/", DogDescriptionAPIView.as_view()),
]
