from djongo import models
from server.models import BaseUser, Organization


class OrganizationReview(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    comment = models.CharField(max_length=500)
    image = models.CharField(max_length=500, default="")
    createdAt = models.DateField(auto_now_add=True)
    organization = models.EmbeddedField(model_container=Organization)
    user = models.EmbeddedField(model_container=BaseUser)
