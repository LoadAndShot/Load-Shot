from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    can_access_catalogue1 = models.BooleanField(default=False)
    can_access_catalogue2 = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=128, blank=True, null=True)  # Numéro IG, libre

    def __str__(self):
        return self.username

