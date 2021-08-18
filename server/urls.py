from django.urls import path, re_path
from . import views

urlpatterns = [
    path("user/signup", views.SignupView.as_view()),
    path("user/signin", views.signin),
    path("user/kakao", views.kakao),
    path("refresh", views.refresh),
    path("airport/<str:name>", views.AirportAPIView.as_view()),
    path("dog/list/", views.DogAPIView.as_view()),
    path("dog/description/", views.DogDescriptionAPIView.as_view()),
    path("dog/image/", views.DogImageAPIView.as_view()),
    path("upload/test", views.upload_test),
    path("review/user", views.UserReviewAPIView.as_view()),
]
