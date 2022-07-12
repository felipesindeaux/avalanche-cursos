from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404, render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.views import APIView, Response, status

from .mixins import SerializerByMethodMixin
from .models import User
from .serializers import (AccountSerializer, LoginSerializer,
                          UpdateAccountSerializer,
                          UpdateStatusAccountSerializer)


class ManagementUserView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UpdateStatusAccountSerializer

    lookup_url_kwarg = 'id'


class ListUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer


class RetrieveUpdateUserView(SerializerByMethodMixin, generics.RetrieveUpdateAPIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_map = {
        "GET": AccountSerializer,
        "PATCH": UpdateAccountSerializer,
    }

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())

        obj = get_object_or_404(queryset, pk=self.request.user.id)

        self.check_object_permissions(self.request, obj)

        return obj


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
