from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    IATA = models.CharField(max_length=5)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.IATA
