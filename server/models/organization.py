from djongo import models
from django import forms


class Image(models.Model):
    url = models.URLField(max_length=200)

    class Meta:
        abstract = True


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ("url",)


class SNS(models.Model):
    sns = models.CharField(max_length=200)
    name = models.CharField(max_length=200)

    class Meta:
        abstract = True


class SNSForm(forms.ModelForm):
    class Meta:
        model = SNS
        fields = ("sns", "name")


class Organization(models.Model):
    name = models.CharField(max_length=100)
    ceo = models.CharField(max_length=100)
    description = models.TextField()
    phone = models.CharField(max_length=100)
    images = models.ArrayField(model_container=Image, model_form_class=ImageForm)
    donation = models.CharField(max_length=100)
    fax = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    sns = models.ArrayField(model_container=SNS, model_form_class=SNSForm)

    class Meta:
        abstract = True


class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = (
            "name",
            "ceo",
            "description",
            "phone",
            "phone",
            "images",
            "donation",
            "fax",
            "email",
            "sns",
        )
