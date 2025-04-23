from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import models
from django.conf import settings

class Product(models.Model):
    CATALOGUE_CHOICES = [
        (1, 'Catalogue 1'),
        (2, 'Catalogue 2'),
    ]

    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    catalogue = models.IntegerField(choices=CATALOGUE_CHOICES)

    def __str__(self):
        return self.name

class Order(models.Model):
    DELIVERY_CHOICES = [
        ('retrait', 'Retrait au magasin'),
        ('livraison', 'Livraison'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande de {self.product.name} par {self.user.username}"

class CustomUser(AbstractUser):
    is_locked_catalogue1 = models.BooleanField(default=False)
    is_locked_catalogue2 = models.BooleanField(default=False)

    def __str__(self):
        return self.username

