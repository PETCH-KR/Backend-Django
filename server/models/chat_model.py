"""
_id
room_name (chatroom_id)
createdAt
message
sender(user or organization _id)
"""


# from django.db import models
from djongo import models
from .organization_model import AbstractOrganization
from .user_model import AbstractBaseUser

class AbstractMessage(models.Model):
    

class Application(models.Model):
    _id = models.ObjectIdField(primary_key=True, db_column="_id")
    room_name = models.CharField(null=False, max_length=30)
    message = models.

    user = models.EmbeddedField(model_container=AbstractBaseUser)
    Organization = models.EmbeddedField(model_container=AbstractOrganization)
    createdAt = models.DateField(auto_now_add=True)

    objects = models.DjongoManager()