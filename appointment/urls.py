from django.urls import path

from .views import (
    AppointmentDetailView,
    AppointmentListView,
    AppointmentUpdateView,
    DeleteAppointmentView,
    ScheduleAppointmentView,
)

urlpatterns = [
    path(
        "schedule-appointment/",
        ScheduleAppointmentView.as_view(),
        name="schedule_appointment",
    ),
    path("list/", AppointmentListView.as_view(), name="list"),
    path("delete/<int:pk>/", DeleteAppointmentView.as_view(), name="delete"),
    path("<pk>/", AppointmentDetailView.as_view(), name="detail"),
    path("update/<pk>/", AppointmentUpdateView.as_view(), name="update"),
]
