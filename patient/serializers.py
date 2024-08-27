from rest_framework import serializers

from .models import CustomUser


class InitialRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "name", "phoneNumber"]


class CompleteRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},  # Ensure password is write-only
        }

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user
