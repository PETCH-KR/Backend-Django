# from django.db import models
from djongo import models
from .organization_model import AbstractOrganization, OrganizationForm
from django import forms


class AbstractDog(models.Model):
    _id = models.ObjectIdField(primary_key=True, db_column="_id")
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    deadline = models.DateField(auto_now_add=False)
    createdAt = models.DateField(auto_now_add=True)
    destination = models.CharField(max_length=100)
    image = models.CharField(max_length=10000)

    organization = models.EmbeddedField(
        model_container=AbstractOrganization, model_form_class=OrganizationForm
    )

    objects = models.DjongoManager()

    class Meta:
        abstract = True


class Dog(AbstractDog):
    objects = models.DjongoManager()

    class Meta:
        ordering = ["name"]
