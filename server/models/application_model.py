# from django.db import models
from djongo import models
from .organization_model import OrganizationForm
from .dog_model import AbstractDog, Dog


class Application(models.Model):
    _id = models.ObjectIdField(primary_key=True)
    motivation = models.CharField(maxlength=500)
    resume = models.CharField(max_length=1000)
    departure = models.CharField(max_length=10)
    destination = models.CharField(max_length=10)
    departureDate = models.DateField(auto_now_add=False)
    arrivalDate = models.DateField(auto_now_add=False)
    dog = models.EmbeddedField(model_container=AbstractDog)
    userEmail = model.CharField(max_length=100)
    objects = models.DjongoManager()
