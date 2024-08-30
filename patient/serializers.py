from rest_framework import serializers

from .models import CustomUser


class InitialRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "name", "phone"]


class CompleteRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    identificationDocument = serializers.FileField(required=False)

    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
            "identificationDocument": {"required": False},  # Optional field
        }

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        identification_document = validated_data.pop("identificationDocument", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)

        if identification_document:
            user.identificationDocument = identification_document

        user.save()
        return user
