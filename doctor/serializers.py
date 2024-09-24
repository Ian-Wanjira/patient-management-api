from rest_framework import serializers

from accounts.models import CustomUser

from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source="user.id", read_only=True)
    email = serializers.EmailField(source="user.email")
    name = serializers.CharField(source="user.name")
    phone = serializers.CharField(source="user.phone")
    password = serializers.CharField(write_only=True, source="user.password")

    image = serializers.ImageField()

    class Meta:
        model = Doctor
        fields = ["id", "email", "name", "phone", "password", "image"]

    def create(self, validated_data):
        # Extract user data from the flattened fields
        user_data = validated_data.pop("user")
        user = CustomUser.objects.create_user(**user_data)
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor
