from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

from users.utils import CustomUserManager


class User(AbstractUser):
    name = models.CharField(max_length=127)
    email = models.EmailField(unique=True)
    is_teacher = models.BooleanField()

    username = None
    first_name = None
    last_name = None

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_message = """
        Foi recebida uma requisição para troca de senha
        Caso não tenha realiza-a, ignore esta mensagem

        O token para trocar sua senha é: {token}

        Primeiro envie seu email mais sua nova senha para /api/users/password_reset/?token={token}
        Depois envie o token junto a nova senha para /api/users/password_reset/confirm/
    """.format(token=reset_password_token.key)

    send_mail(
        "Password Reset for Avalanche Cursos",
        email_message,
        None,
        [reset_password_token.user.email]
    )
