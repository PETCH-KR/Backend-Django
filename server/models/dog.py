# from django.db import models
from djongo import models
from .organization import Organization, OrganizationForm


class Dog(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    deadline = models.DateField()
    creaatedAt = models.DateField(auto_now_add=True)
    destination = models.CharField(max_length=100)

    organization = models.EmbeddedField(
        model_container=Organization, model_form_class=OrganizationForm
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name