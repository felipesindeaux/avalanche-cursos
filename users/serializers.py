from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "is_teacher",
            "password"
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):

        if User.objects.filter(email__iexact=validated_data["email"]).exists():
            raise serializers.ValidationError()

        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "is_teacher",
            "password",
            "is_active"
        ]
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = [
            "is_teacher",
        ]


# Serializer de ativação/desativação de usuários (somente ADM)
class UpdateUserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "email",
            "is_teacher",
            "password",
            "is_active"
        ]
        read_only_fields = [
            "id",
            "name",
            "email",
            "is_teacher",
            "password"
        ]
