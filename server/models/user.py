from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):

    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128, null=True)
    phone = models.CharField(max_length=15, null=True)
    passport = models.BooleanField(default=False)
    # provider = DEFAULT | APPLE | GOOGLE | KAKAO
    provider = models.CharField(max_length=20, default="DEFAULT")
    token = models.CharField(max_length=255, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
