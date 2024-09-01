from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer


class RegistrationView(APIView):
    def post(self, request):
        print("Request Data: ", request.data)
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
