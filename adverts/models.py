from django.db import models
from djmoney.models.fields import MoneyField
from .validators import (
    validate_icon,
    images_path,
)

# Create your models here.
class Location(models.Model):
    address = models.CharField(
        max_length = 63,
        verbose_name = "Адрес",
    )

    latitude = models.DecimalField(
        max_digits = 9, 
        decimal_places = 6,
        verbose_name = "Широта",
    )

    longitude = models.DecimalField(
        max_digits = 9, 
        decimal_places = 6,
        verbose_name = "Долгота",
    )

    created = models.DateTimeField(
        verbose_name = "Создано",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Обновлено",
        auto_now = True,
    )


class Category(models.Model):
    icon = models.FileField(
        upload_to = 'category/icons/', 
        validators = [validate_icon],
        verbose_name = "Иконка",
    )
    
    title = models.CharField(
        max_length = 63,
        verbose_name = "Название",
    )

    created = models.DateTimeField(
        verbose_name = "Создано",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Обновлено",
        auto_now = True,
    )


class Advert(models.Model):
    profile = models.ForeignKey(
        'profiles.Profile',
        on_delete = models.CASCADE,
        related_name = 'adverts',
        verbose_name = "Профиль",
    )

    title = models.CharField(
        max_length = 63,
        verbose_name = "Заголовок",
    )

    category = models.ForeignKey(
        Category, 
        on_delete = models.CASCADE,
        related_name = 'adverts',
        verbose_name = "Категория",
    )

    images = models.ImageField(
        upload_to = images_path,
        null = True, 
        blank = True,
        verbose_name = "Изображения",
    )

    description = models.TextField(
        verbose_name = "Описание",
    )

    price = MoneyField(
        max_digits = 8, 
        decimal_places = 0,
        default_currency = 'KZT',
        verbose_name = "Вознаграждение",
    )

    location = models.OneToOneField(
        Location, 
        on_delete = models.CASCADE,
        related_name = 'advert',
        verbose_name = "Местоположение",
    )

    is_active = models.BooleanField(
        default = True,
        verbose_name = "Статус",
    )

    created = models.DateTimeField(
        verbose_name = "Создано",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Обновлено",
        auto_now = True,
    )