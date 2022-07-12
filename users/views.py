from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, Response, status

from .models import User
from .serializers import (AccountSerializer, LoginSerializer,
                          UpdateAccountSerializer,
                          UpdateStatusAccountSerializer)

class ListUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer

class RetrieveUserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password']
        )

        if user:
            token = Token.objects.get_or_create(user=user)[0]

            return Response({'token': token.key})

        return Response({"detail": 'invalid email or password'}, status.HTTP_401_UNAUTHORIZED)
