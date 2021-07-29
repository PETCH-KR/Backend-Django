# from django.db import models
from djongo import models
from organization import organization


class dog(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    descriptiokn = models.CharField(max_length=100)
    deadline = models.DateField()
    creaatedAt = models.DateField(auto_now_add=True)
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    organization = models.EmbeddedField(model_container=organization)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.IATA

e = dog(name='hi', organization=None)
e.clean_fields()