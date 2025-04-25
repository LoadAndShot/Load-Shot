from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=100, blank=True)
    can_access_catalogue1 = models.BooleanField(default=False)
    can_access_catalogue2 = models.BooleanField(default=False)

    def __str__(self):
        return self.username

