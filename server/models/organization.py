from djongo import models
from django import forms


class image(models.Model):
    url = models.URLField(max_length=200)

    class Meta:
        abstract = True


class imageForm(forms.ModelForm):
    class Meta:
        model = image
        fields = "url"


class sns(models.Model):
    sns = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True


class snsForm(forms.ModelForm):
    class Meta:
        model = sns
        fields = ("sns", "name")


class organization(models.Model):
    name = models.CharField(max_length=100)
    ceo = models.CharField(max_length=100)
    description = models.TextField()
    phone = models.CharField(max_length=100)
    images = models.ArrayField(model_container=image, model_form_class=imageForm)
    donation = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    sns = models.ArrayField(model_container=sns, model_form_class=snsForm)
