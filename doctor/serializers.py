from rest_framework import serializers

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = "__all__"

    def create(self, validated_data):
        doctor = Doctor.objects.create(**validated_data)
        return doctor
