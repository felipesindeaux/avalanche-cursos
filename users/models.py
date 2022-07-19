import uuid

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
from django.db import models
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from drf_spectacular.utils import extend_schema

from users.utils import CustomUserManager


class User(AbstractUser):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=127)
    email = models.EmailField(unique=True)
    is_teacher = models.BooleanField()

    username = None
    first_name = None
    last_name = None

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    email_message = """
        Olá {name}, tudo bem?
        
        Foi recebida uma requisição para troca de senha da sua conta
        Caso não tenha realizado-a, ignore esta mensagem

        O token para trocar sua senha é: {token}
    """.format(
        name=reset_password_token.user.name.title(), token=reset_password_token.key
    )

    send_mail(
        "Password Reset for Avalanche Cursos",
        email_message,
        None,
        [reset_password_token.user.email],
    )
