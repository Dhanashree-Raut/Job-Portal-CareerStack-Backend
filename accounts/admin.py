from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # Fields to show in the user list in admin panel
    list_display = ['email', 'username', 'role', 'is_active']
    list_filter = ['role', 'is_active']

    # Add role field to the admin edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Profile', {
            'fields': ('role', 'phone', 'profile_picture', 'skills', 'resume',
                      'company_name', 'company_website', 'company_description')
        }),
    )