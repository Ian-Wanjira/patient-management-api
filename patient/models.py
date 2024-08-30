import uuid

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        if password:  # Only set the password if provided
            user.set_password(password)
        else:
            user.set_unusable_password()  # Set an unusable password if none is provided

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    GENDER_CHOICES = [
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None  # Remove username field as we're using email for authentication
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)

    # Optional fields to be filled out later
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        blank=True,
        null=True,
    )
    privacyConsent = models.BooleanField(default=False)
    address = models.CharField(max_length=100, blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    emergencyContactName = models.CharField(max_length=100, blank=True, null=True)
    emergencyContactPhone = models.CharField(max_length=15, blank=True, null=True)
    insuranceProvider = models.CharField(max_length=100, blank=True, null=True)
    insurancePolicyNumber = models.CharField(max_length=100, blank=True, null=True)
    allergies = models.TextField(blank=True, null=True)
    currentMedications = models.TextField(blank=True, null=True)
    familyMedicalHistory = models.TextField(blank=True, null=True)
    pastMedicalHistory = models.TextField(blank=True, null=True)
    identificationType = models.CharField(max_length=100, blank=True, null=True)
    identificationNumber = models.CharField(max_length=100, blank=True, null=True)
    # identificationDocumentId = models.CharField(max_length=100, blank=True, null=True)
    # identificationDocumentUrl = models.URLField(blank=True, null=True)
    identificationDocument = models.FileField(
        upload_to="identification_documents/", blank=True, null=True
    )
    primaryCarePhysician = models.CharField(max_length=100, blank=True, null=True)
    dateOfBirth = models.DateField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "phone"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.name}"
