from turtle import update
from venv import create
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import NotAcceptable
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView, Response, status
from drf_spectacular.utils import extend_schema

from .mixins import SerializerByMethodMixin
from .models import User
from .serializers import (LoginSerializer, UpdateUserSerializer,
                          UpdateUserStatusSerializer, UserSerializer)
@extend_schema(tags=['Users'])
class ManagementUserView(generics.UpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UpdateUserStatusSerializer

    lookup_url_kwarg = "id"

    def perform_update(self, serializer):
        user = get_object_or_404(User, pk=self.kwargs["id"])
        if self.request.user != user:
            serializer.save()
        else:
            raise NotAcceptable("You cannot deactivate yourself.")

@extend_schema(tags=['Users'])
class ListUsersView(generics.ListAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    queryset = User.objects.all()
    serializer_class = UserSerializer

@extend_schema(tags=['Users'])
class RetrieveUpdateUserView(SerializerByMethodMixin, generics.RetrieveUpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer
    serializer_map = {
        "GET": UserSerializer,
        "PATCH": UpdateUserSerializer,
    }

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        obj = get_object_or_404(queryset, pk=self.request.user.id)

        self.check_object_permissions(self.request, obj)

        return obj

@extend_schema(tags=['Users'])
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@extend_schema(tags=['Login'])
class LoginView(APIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer

    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["email"],
            password=serializer.validated_data["password"],
        )

        if user:
            token = Token.objects.get_or_create(user=user)[0]

            return Response({"token": token.key})

        return Response(
            {"detail": "invalid email or password"}, status.HTTP_401_UNAUTHORIZED
        )
