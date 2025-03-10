from django.contrib import admin
from .models import (
    Advert,
    Category,
)

# Register your models here.

class AdvertAdmin(admin.ModelAdmin):
   pass

# Register the AppUser model with the custom admin class
admin.site.register(Advert, AdvertAdmin)

class CategoryAdmin(admin.ModelAdmin):
   pass

# Register the AppUser model with the custom admin class
admin.site.register(Category, CategoryAdmin)