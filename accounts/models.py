from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    # Ici tu peux ajouter des champs si tu veux, exemple :
    # phone_number = models.CharField(max_length=20, blank=True, null=True)
    pass
