from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Si tu veux rajouter des champs personnalisés plus tard, c’est ici
    pass

