from django.urls import path

from .views import DeleteDoctorView, DoctorListView, RegistrationView

urlpatterns = [
    path("doctor-registration/", RegistrationView.as_view(), name="register"),
    path("list/", DoctorListView.as_view(), name="list"),
    path("delete/<pk>/", DeleteDoctorView.as_view(), name="delete"),
]
