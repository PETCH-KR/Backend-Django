from djongo import models
from server.models import BaseUser, AbstractOrganization


class UserReview(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    comment = models.CharField(max_length=500)
    image = models.CharField(max_length=1000, default="")
    createdAt = models.DateField(auto_now_add=True)
    organization = models.EmbeddedField(model_container=AbstractOrganization)
    user = models.EmbeddedField(model_container=BaseUser)

    objects = models.DjongoManager()
