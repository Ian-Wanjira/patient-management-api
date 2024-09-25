from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Patient
from .serializers import PatientSerializer

User = get_user_model()


class RegisterPatientView(APIView):
    def post(self, request):
        print("Request Data: ", request.data)
        serializer = PatientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PatientListView(APIView):
    def get(self, request):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class DeletePatientView(APIView):
    def delete(self, request, pk):
        user = User.objects.get(id=pk)
        patient = Patient.objects.get(user=user)
        patient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
