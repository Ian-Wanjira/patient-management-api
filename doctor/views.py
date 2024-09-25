from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Doctor
from .serializers import DoctorSerializer

User = get_user_model()


class RegistrationView(APIView):
    def post(self, request):
        print("Request Data: ", request.data)
        serializer = DoctorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DoctorListView(APIView):
    def get(self, request):
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteDoctorView(APIView):
    def delete(self, request, pk):
        user = User.objects.get(id=pk)
        doctor = Doctor.objects.get(user=user)
        doctor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
