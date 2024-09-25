from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import DeletePatientView, PatientListView, RegisterPatientView

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "patient-registration/",
        RegisterPatientView.as_view(),
        name="register_patient",
    ),
    path("list/", PatientListView.as_view(), name="list"),
    path("delete/<pk>/", DeletePatientView.as_view(), name="delete"),
]
