from django.contrib.auth.models import AbstractBaseUser
from django.db import models


class User(AbstractBaseUser):

    email = models.EmailField(
        max_length=100, unique=True, verbose_name="Email", help_text="이메일"
    )
    password = models.CharField(
        max_length=128, null=True, verbose_name="password", help_text="비밀번호"
    )
    phone = models.CharField(
        max_length=15, null=True, verbose_name="phone", help_text="전화번호"
    )
    passport = models.BooleanField(
        default=False, verbose_name="passport", help_text="여권"
    )
    # provider = DEFAULT | APPLE | GOOGLE | KAKAO
    provider = models.CharField(
        max_length=20,
        default="DEFAULT",
        verbose_name="provider",
        help_text="DEFAULT | APPLE | GOOGLE | KAKAO",
    )
    token = models.CharField(
        max_length=255, null=True, verbose_name="token", help_text="Refresh Token"
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
