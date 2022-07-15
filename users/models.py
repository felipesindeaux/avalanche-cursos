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
        Olá {name}, tudo bem?
        Foi recebida uma requisição para troca de senha
        Caso não tenha realiza-a, ignore esta mensagem

        O token para trocar sua senha é: {token}
    """.format(name=reset_password_token.user.name, token=reset_password_token.key)

    send_mail(
        # assunto do email
        "Password Reset for Avalanche Cursos",
        # corpo do email
        email_message,
        # endereço de email de quem enviará o email (se None, pegará de EMAIL_HOST_USER)
        None,
        # lista dos endereços de email que receberão o email
        [reset_password_token.user.email]
    )
