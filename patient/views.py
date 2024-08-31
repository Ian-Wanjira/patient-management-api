import json

from rest_framework import generics, status
from rest_framework.exceptions import NotFound
from rest_framework.parsers import FormParser, MultiPartParser
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
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self):
        # Retrieve the user by userId from the request data
        user_id = self.request.data.get("id")
        if not user_id:
            raise NotFound("User ID is required to complete registration")
        try:
            return CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found")

    def put(self, request, *args, **kwargs):
        # Debugging: print request data to ensure it's being received correctly
        print("Request Data:", request.data)
        print("Files: ", request.FILES)
        user_id = request.data.get("id")
        if not user_id:
            raise NotFound("User ID is required to complete registration")

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            raise NotFound("User not found")

        json_data = request.data.get("json")
        if json_data:
            json_data = json.loads(json_data)
            request.data.update(json_data)

        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        # Issue JWT tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response(
            {
                "status": "User updated successfully",
                "refresh": str(refresh),
                "access": str(access_token),
            },
            status=status.HTTP_200_OK,
        )

    def perform_update(self, serializer):
        serializer.save()  # Save the instance


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
