from django.contrib import admin

# Register your models here.
from .models import (
    Profile,
)

class ProfileAdmin(admin.ModelAdmin):
   pass

# Register the AppUser model with the custom admin class
admin.site.register(Profile, ProfileAdmin)