from django.contrib.auth.models import AbstractUser
from django.db import models

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
