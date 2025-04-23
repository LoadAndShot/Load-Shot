from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    can_access_catalogue1 = models.BooleanField(default=True)
    can_access_catalogue2 = models.BooleanField(default=True)

