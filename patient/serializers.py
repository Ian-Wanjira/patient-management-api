from rest_framework import serializers

from .models import CustomUser


class InitialRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "name", "phone"]


class CompleteRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)

        # Debug: Check what's inside validated_data
        print("Validated Data:", validated_data)

        # Update the instance with the validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if password:
            instance.set_password(password)

        instance.save()
        return instance
