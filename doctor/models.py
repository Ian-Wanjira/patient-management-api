import uuid

from django.db import models


class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    image = models.ImageField(upload_to="doctor_images")

    def __str__(self):
        self.email
