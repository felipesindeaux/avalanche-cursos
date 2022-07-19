from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "email", "is_teacher", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):

        if User.objects.filter(email__iexact=validated_data["email"]).exists():
            raise serializers.ValidationError()

        return User.objects.create_user(**validated_data)


class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name"]


class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        exclude = (
            "is_active",
            "last_login",
            "is_superuser",
            "is_staff",
            "date_joined",
            "groups",
            "user_permissions",
        )
        extra_kwargs = {"password": {"write_only": True}}
        read_only_fields = [
            "is_teacher",
        ]


# Serializer de ativação/desativação de usuários (somente ADM)
class UpdateUserStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["is_active"]
