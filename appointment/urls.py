from django.urls import path

from .views import AppointmentListView, DeleteAppointmentView, ScheduleAppointmentView

urlpatterns = [
    path(
        "schedule-appointment/",
        ScheduleAppointmentView.as_view(),
        name="schedule_appointment",
    ),
    path("list/", AppointmentListView.as_view(), name="list"),
    path("delete/<int:pk>/", DeleteAppointmentView.as_view(), name="delete"),
]
