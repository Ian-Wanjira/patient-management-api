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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["patient"] = PatientSerializer(instance.patient).data
        representation["doctor"] = DoctorSerializer(instance.doctor).data
        return representation
