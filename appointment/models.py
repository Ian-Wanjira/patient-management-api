from django.db import models

from doctor.models import Doctor
from patient.models import Patient


class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("scheduled", "Scheduled"),
        ("cancelled", "Cancelled"),
    ]

    patient = models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name="appointments"
    )
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="appointments"
    )
    schedule = models.DateTimeField()
    reason = models.TextField(max_length=500)
    notes = models.TextField(max_length=500, blank=True, null=True)
    cancellationReason = models.TextField(max_length=500, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
