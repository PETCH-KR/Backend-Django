from django.db import models


class Airport(models.Model):
    name = models.CharField(max_length=100, verbose_name="공항명", help_text="공항명")
    country = models.CharField(max_length=100, verbose_name="국가", help_text="국가")
    IATA = models.CharField(max_length=5, verbose_name="IATA", help_text="IATA")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.IATA
