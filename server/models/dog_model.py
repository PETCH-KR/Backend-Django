# from django.db import models
from djongo import models
from .organization_model import AbstractOrganization, OrganizationForm
from django.conf import settings
from djongo.storage import GridFSStorage


class Dog(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    deadline = models.DateField()
    createdAt = models.DateField(auto_now_add=True)
    destination = models.CharField(max_length=100)
    image = models.CharField(max_length=10000)

    organization = models.EmbeddedField(
        model_container=AbstractOrganization, model_form_class=OrganizationForm
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
