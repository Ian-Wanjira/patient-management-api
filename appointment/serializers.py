from rest_framework import serializers

from doctor.models import Doctor
from doctor.serializers import DoctorSerializer
from patient.models import Patient
from patient.serializers import PatientSerializer

from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.UUIDField()
    doctor = serializers.UUIDField()

    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "doctor",
            "schedule",
            "reason",
            "notes",
            "cancellationReason",
            "status",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        patient_uuid = validated_data.pop("patient")
        doctor_uuid = validated_data.pop("doctor")

        # Fetch the Patient and Doctor instances using the UUID
        patient = Patient.objects.get(user__pk=patient_uuid)
        doctor = Doctor.objects.get(user__pk=doctor_uuid)

        # Create the appointment with the fetched instances
        appointment = Appointment.objects.create(
            patient=patient, doctor=doctor, **validated_data
        )
        return appointment

    def update(self, instance, validated_data):
        patient_uuid = validated_data.pop("patient", None)
        doctor_uuid = validated_data.pop("doctor", None)

        if patient_uuid:
            patient = Patient.objects.get(user__pk=patient_uuid)
            instance.patient = patient

        if doctor_uuid:
            doctor = Doctor.objects.get(user__pk=doctor_uuid)
            instance.doctor = doctor

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["patient"] = PatientSerializer(instance.patient).data
        representation["doctor"] = DoctorSerializer(instance.doctor).data
        return representation
