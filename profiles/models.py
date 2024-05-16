from django.db import models
from .validators import (
    images_path,
)

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        'users.AppUser',
        on_delete = models.CASCADE,
        verbose_name = "Пользователь",
        related_name = 'profile',
    )
    
    profile_image = models.ImageField(
        upload_to = images_path,
        verbose_name = "Изображение",
        null = True,
        blank = True,
    )

    created = models.DateTimeField(
        verbose_name = "Создано",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Обновлено",
        auto_now = True,
    )