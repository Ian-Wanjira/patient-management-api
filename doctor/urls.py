from django.urls import path

from .views import DoctorListView, RegistrationView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("list/", DoctorListView.as_view(), name="list"),
]
