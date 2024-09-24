from cloudinary.models import CloudinaryField
from django.db import models

from accounts.models import CustomUser


class Doctor(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="doctor_profile"
    )
    image = CloudinaryField("image", blank=True, null=True)
