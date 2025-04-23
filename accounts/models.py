from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_locked_catalogue1 = models.BooleanField(default=False)
    is_locked_catalogue2 = models.BooleanField(default=False)
