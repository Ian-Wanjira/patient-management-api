from rest_framework import serializers

from .models import CustomUser

# class RegistrationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = get_user_model()
#         fields = "__all__"

#         extra_kwargs = {
#             "password": {"write_only": True},
#         }

#     def create(self, validated_data):
#         patient = CustomUser.objects.create_user(**validated_data)
#         return patient


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


# class PatientSerializer(serializers.ModelSerializer):
#     user = CustomUserSerializer()

#     class Meta:
#         model = Patient
#         fields = "__all__"

#     def create(self, validated_data):
#         user_data = validated_data.pop("user")
#         user = CustomUser.objects.create_user(**user_data)
#         patient = Patient.objects.create(user=user, **validated_data)
#         return patient


# class DoctorSerializer(serializers.ModelSerializer):
#     user = CustomUserSerializer()

#     class Meta:
#         model = Doctor
#         fields = "__all__"

#     def create(self, validated_data):
#         user_data = validated_data.pop("user")
#         user = CustomUser.objects.create_user(**user_data)
#         doctor = Patient.objects.create(user=user, **validated_data)
#         return doctor
