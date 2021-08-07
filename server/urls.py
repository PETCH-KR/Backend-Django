from django.urls import path
from . import views

urlpatterns = [
    path("user/signup", views.SignupView.as_view()),
    path("user/signin", views.signin),
    path("user/kakao", views.kakao),
    path("refresh", views.refresh),
    path("airport/<str:name>/", views.AirportAPIView.as_view()),
    path("upload/test", views.upload_test),
]
