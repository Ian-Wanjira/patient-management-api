from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"

        extra_kwargs = {
            "password": {"write_only": True},
        }

    def create(self, validated_data):
        patient = CustomUser.objects.create_user(**validated_data)
        return patient
