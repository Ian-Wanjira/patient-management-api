from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the admin interface
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("name", "phoneNumber", "dateOfBirth", "address")},
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "phoneNumber", "password1", "password2"),
            },
        ),
    )
    list_display = ("email", "name", "is_staff", "is_superuser")
    search_fields = ("email", "name")
    ordering = ("email",)


admin.site.register(CustomUser, CustomUserAdmin)
