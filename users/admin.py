from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import AppUser

class AppUserAdmin(UserAdmin):
    # Specify fields to be displayed in the admin list view
    list_display = ('phone_number', 'first_name', 'last_name', 'is_active')

    # Specify default ordering of objects in the admin list view
    ordering = ('-created',)

    # Specify fields to be used in the change list and filter dropdowns
    list_filter = ('is_active', 'is_staff', 'created', 'updated')

    # Specify fields to be displayed in the detail view
    fieldsets = (
        (None, {'fields': ('phone_number', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff')}),
        ('Important dates', {'fields': ('created', 'updated')}),
    )

    # Define fields that will be readonly in the admin detail view
    readonly_fields = ('created', 'updated')

    # Define the search fields for the admin interface
    search_fields = ('phone_number', 'first_name', 'last_name')

# Register the AppUser model with the custom admin class
admin.site.register(AppUser, AppUserAdmin)