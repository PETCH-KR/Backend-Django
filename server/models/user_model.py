from django.contrib.auth.models import AbstractBaseUser
from djongo import models
from django.contrib.auth.models import UserManager
import uuid


class BaseUser(AbstractBaseUser):
    _id = models.ObjectIdField(primary_key=True, db_column="_id")
    email = models.EmailField(
        max_length=100,
        unique=True,
        verbose_name="Email",
        help_text="이메일",
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

    class Meta:
        abstract = True


class User(BaseUser):
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
