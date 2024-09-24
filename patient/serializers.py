from rest_framework import serializers

from accounts.models import CustomUser

from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    # User fields flattened into the serializer
    id = serializers.UUIDField(source="user.id", read_only=True)
    email = serializers.EmailField(source="user.email")
    name = serializers.CharField(source="user.name")
    phone = serializers.CharField(source="user.phone")
    password = serializers.CharField(write_only=True, source="user.password")

    class Meta:
        model = Patient
        fields = [
            "id",
            "email",
            "name",
            "phone",
            "password",
            "address",
            "occupation",
            "emergencyContactName",
            "emergencyContactPhone",
            "insuranceProvider",
            "insurancePolicyNumber",
            "allergies",
            "currentMedications",
            "familyMedicalHistory",
            "pastMedicalHistory",
            "identificationType",
            "identificationNumber",
            "identificationDocument",
            "primaryCarePhysician",
            "treatmentConsent",
            "disclosureConsent",
            "privacyConsent",
            "dateOfBirth",
        ]

    def create(self, validated_data):
        # Extract user data from the flattened fields
        user_data = validated_data.pop("user")
        user = CustomUser.objects.create_user(**user_data)
        patient = Patient.objects.create(user=user, **validated_data)
        return patient
