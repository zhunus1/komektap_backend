from django.contrib import admin

# Register your models here.
from .models import (
    Location,
    Category,
    Advert,
)


class LocationAdmin(admin.ModelAdmin):
   pass

admin.site.register(Location, LocationAdmin)


class CategoryAdmin(admin.ModelAdmin):
   pass

admin.site.register(Category, CategoryAdmin)


class AdvertAdmin(admin.ModelAdmin):
   pass

admin.site.register(Advert, AdvertAdmin)