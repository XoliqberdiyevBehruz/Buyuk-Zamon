from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status, permissions

from account.auth import serializers


class LoginApiView(GenericAPIView):
    serializer_class = serializers.LoginSerializer

    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data    
            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        