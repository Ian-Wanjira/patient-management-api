from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import CompleteRegistrationView, InitialRegistrationView, PatientProfileView

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "get-started/", InitialRegistrationView.as_view(), name="initial-registration"
    ),
    path(
        "complete-registration/",
        CompleteRegistrationView.as_view(),
        name="complete-registration",
    ),
    path("<uuid:id>/", PatientProfileView.as_view(), name="patient-profile"),
]
