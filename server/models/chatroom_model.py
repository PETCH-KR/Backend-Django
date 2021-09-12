"""
_id
user
organization
createdAt
"""

# from django.db import models
from djongo import models
from .organization_model import AbstractOrganization
from .user_model import BaseUser

class AbstractMessage(models.Model):
    sender = models.CharField(max_length=200)
    messageType = models.CharField(max_length=100)
    message = models.CharField(max_length=1000)
    createAt = models.DateTimeField()

    class Meta:
        abstract = True

class Chatroom(models.Model):
    room_name = models.CharField(primary_key=True, max_length=300)
    user = models.EmbeddedField(model_container=BaseUser)
    organization = models.EmbeddedField(model_container=AbstractOrganization)
    createdAt = models.DateField(auto_now_add=True)
    message = models.ArrayField(model_container=AbstractMessage)

    objects = models.DjongoManager()