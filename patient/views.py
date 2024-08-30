from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import CustomUser
from .serializers import CompleteRegistrationSerializer, InitialRegistrationSerializer


class InitialRegistrationView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = InitialRegistrationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            {"userId": str(user.id)}, status=status.HTTP_201_CREATED, headers=headers
        )


class CompleteRegistrationView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CompleteRegistrationSerializer

    def get_object(self):
        # Retrieve the user by userId from the request data
        user_id = self.request.data.get("userId")
        if not user_id:
            return Response(
                {"error": "userId is required to complete registration."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return generics.get_object_or_404(CustomUser, id=user_id)

    def perform_update(self, serializer):
        user = self.get_object()

        # Save all fields (including password if provided)
        updated_user = serializer.save(instance=user)

        # Check and update the password if it was provided
        password = self.request.data.get("password")
        if password:
            updated_user.set_password(password)
            updated_user.save()

        # Issue JWT tokens upon successful registration completion
        refresh = RefreshToken.for_user(updated_user)
        access_token = refresh.access_token

        return Response(
            {
                "status": "User updated successfully",
                "refresh": str(refresh),
                "access": str(access_token),
            },
            {"userId": str(user.id)},
            status=status.HTTP_200_OK,
        )


class PatientProfileView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = InitialRegistrationSerializer
    permission_classes = []

    def get_object(self):
        user_id = self.kwargs.get("id")
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found")
