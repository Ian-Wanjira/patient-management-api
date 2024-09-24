from django.db import models

from accounts.models import CustomUser


class Patient(models.Model):
    GENDER_CHOICES = [("male", "Male"), ("female", "Female"), ("other", "Other")]

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="patient_profile"
    )

    gender = models.CharField(
        max_length=10, choices=GENDER_CHOICES, blank=True, null=True
    )
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
    identificationDocument = models.FileField(
        upload_to="identification_documents/", blank=True, null=True
    )
    primaryCarePhysician = models.CharField(max_length=100, blank=True, null=True)
    treatmentConsent = models.BooleanField(default=False)
    disclosureConsent = models.BooleanField(default=False)
    privacyConsent = models.BooleanField(default=False)
    dateOfBirth = models.DateField(null=True, blank=True)
