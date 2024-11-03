from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Appointment
from .serializers import AppointmentSerializer
from .tasks import send_sms_notification


class ScheduleAppointmentView(APIView):
    def post(self, request):
        serializer = AppointmentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AppointmentListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"


class AppointmentListView(APIView):
    pagination_class = AppointmentListPagination

    def get(self, request):
        try:
            appointments = Appointment.objects.all()
            # Get count of appointments by status
            scheduled_count = appointments.filter(status="scheduled").count()
            cancelled_count = appointments.filter(status="cancelled").count()
            pending_count = appointments.filter(status="pending").count()
            paginator = self.pagination_class()
            result_page = paginator.paginate_queryset(appointments, request)
            serializer = AppointmentSerializer(result_page, many=True)

            # Get paginated response and add status counts
            response = paginator.get_paginated_response(serializer.data)
            response.data["scheduled_count"] = scheduled_count
            response.data["cancelled_count"] = cancelled_count
            response.data["pending_count"] = pending_count

            return response
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AppointmentDetailView(APIView):
    def get(self, request, pk):
        try:
            appointment = Appointment.objects.get(id=pk)
        except Appointment.DoesNotExist:
            return Response(
                {"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AppointmentUpdateView(APIView):
    def put(self, request, pk):
        try:
            appointment = Appointment.objects.get(id=pk)
        except Appointment.DoesNotExist:
            return Response(
                {"error": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND
            )

        previous_status = appointment.status
        serializer = AppointmentSerializer(appointment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        new_status = serializer.data["status"]

        # Check if the status was changed to "scheduled" or "cancelled"
        if previous_status != new_status and new_status in ["scheduled", "cancelled"]:
            # Customize the message based on the new status
            if new_status == "scheduled":
                status_message = (
                    f"Hello {appointment.patient.user.name}, your appointment with Dr. "
                    f"{appointment.doctor.user.name} has been scheduled for {appointment.schedule}."
                )
            elif new_status == "cancelled":
                status_message = (
                    f"Hello {appointment.patient.user.name}, your appointment with Dr. "
                    f"{appointment.doctor.user.name} on {appointment.schedule} has been cancelled."
                )

            # Schedule the SMS notification task
            send_sms_notification.delay(appointment.id, status_message)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteAppointmentView(APIView):
    def delete(self, request, pk):
        appointment = Appointment.objects.get(id=pk)
        appointment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
