from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the admin interface
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("name", "phone", "dateOfBirth", "address")},
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        ("Identification", {"fields": ("id",)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "name", "phone", "password1", "password2"),
            },
        ),
    )
    list_display = ("id", "email", "name", "is_staff", "is_superuser")
    search_fields = ("id", "email", "name")
    ordering = ("email",)

    # Prevent 'date_joined' from being editable
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing user
            return self.readonly_fields + ("date_joined", "id")
        return self.readonly_fields

    readonly_fields = ("date_joined", "id")


admin.site.register(CustomUser, CustomUserAdmin)
