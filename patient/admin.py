from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {"fields": ("name", "phone", "dateOfBirth", "address", "gender")},
        ),
        (
            "Medical info",
            {
                "fields": (
                    "emergencyContactName",
                    "emergencyContactPhone",
                    "insuranceProvider",
                    "insurancePolicyNumber",
                    "allergies",
                    "currentMedications",
                    "familyMedicalHistory",
                    "pastMedicalHistory",
                    "identificationType",
                    "identificationNumber",
                    "identificationDocument",
                    "primaryCarePhysician",
                )
            },
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

    list_display = (
        "id",
        "email",
        "name",
        "phone",
        "is_staff",
        "is_superuser",
        "gender",
        "dateOfBirth",
        "address",
    )
    search_fields = ("id", "email", "name", "phone")
    ordering = ("email",)

    readonly_fields = ("date_joined", "id")


admin.site.register(CustomUser, CustomUserAdmin)
