from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):

    email = models.CharField(max_length=100, unique=True)
    phone = models.CharField(max_length=15)
    passport = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
