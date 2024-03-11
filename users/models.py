from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from .managers import AppUserManager
from django.contrib.auth.models import (
    AbstractBaseUser, 
    PermissionsMixin
)


# Create your models here.

class AppUser(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(
        unique = True,
    )

    first_name = models.CharField(
        max_length = 30,
    )

    last_name = models.CharField(
        max_length = 30,
    )

    is_active = models.BooleanField(
        default = False,
    )

    is_staff = models.BooleanField(
        default = False,
    )

    created = models.DateTimeField(
        verbose_name = "Создано",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Обновлено",
        auto_now = True,
    )

    USERNAME_FIELD = 'phone_number'

    objects = AppUserManager()

    def __str__(self):
        return str(self.phone_number)