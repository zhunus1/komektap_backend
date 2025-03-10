from django.db import models
from django.contrib.gis.db import models as gis_models
from djmoney.models.fields import MoneyField
from django.core.exceptions import ValidationError


def validate_svg(value):
    """Ensure the uploaded file is an SVG image."""
    if not value.name.lower().endswith('.svg'):
        raise ValidationError("Only SVG files are allowed.")


# Create your models here.
class Category(models.Model):
    title = models.CharField(
        max_length = 255,
    )

    icon = models.FileField(
        upload_to = 'category/icons/',
        validators=[validate_svg],
    )

    def __str__(self):
        return self.title


class Images(models.Model):
    image = models.ImageField(
        upload_to = 'advert/images/',
    )
        
    advert = models.ForeignKey(
        "Advert", 
        on_delete = models.CASCADE, 
        related_name = "images",
    )

    def __str__(self):
        return f"Image {self.pk}"


class Advert(models.Model):
    title = models.CharField(
        max_length = 255,
    )

    profile = models.ForeignKey(
        'profiles.Profile', 
        on_delete=models.CASCADE,
    )

    category = models.ManyToManyField(
        Category, 
        related_name = 'adverts',
    )

    description = models.TextField()

    price = MoneyField(
        max_digits = 10, 
        decimal_places = 0, 
        default_currency = 'KZT',
    )

    location = gis_models.PointField()

    is_active = models.BooleanField(
        default = True,
    )

    def __str__(self):
        return self.title
