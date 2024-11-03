# appointment/tasks.py
from celery import shared_task
from django.conf import settings
from twilio.rest import Client

from .models import Appointment


@shared_task
def send_sms_notification(appointment_id, status_message):
    try:
        appointment = Appointment.objects.get(id=appointment_id)
        patient_phone = appointment.patient.user.phone

        # Twilio client initialization
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

        # Send SMS
        client.messages.create(
            body=status_message, from_=settings.TWILIO_PHONE_NUMBER, to=patient_phone
        )
    except Exception as e:
        # Log the error
        print(f"Error sending SMS: {e}")
