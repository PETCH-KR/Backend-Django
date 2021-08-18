from django.urls import path, re_path
from . import views

urlpatterns = [
    path("user/signup", views.SignupView.as_view()),
    path("user/signin", views.signin),
    path("user/kakao", views.kakao),
    path("refresh", views.refresh),
    path("airport/<str:name>", views.AirportAPIView.as_view()),
    # path("dog/list/", views.DogBasicAPIView.as_view()),
    path("dog/search/", views.DogSearchAPIView.as_view()),
    path("dog/desc/", views.DogDescriptionAPIView.as_view()),
    path("dog/info/", views.DogInfoAPIView.as_view()),
    path("dog/add/", views.DogAPIView.as_view()),
    path("dog/modify/<str:_id>/", views.DogDetailAPIView.as_view()),
    path("upload/test", views.upload_test),
    path("review/user", views.UserReviewAPIView.as_view()),
]
