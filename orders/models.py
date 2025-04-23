from django.db import models
from django.contrib.auth.models import AbstractUser

# Extension du User de base
class CustomUser(AbstractUser):
    lock_catalogue_1 = models.BooleanField(default=False)
    lock_catalogue_2 = models.BooleanField(default=False)

# Catalogue (1 ou 2)
class Catalogue(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Produit dans le catalogue
class Product(models.Model):
    catalogue = models.ForeignKey(Catalogue, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# Commande
class Order(models.Model):
    DELIVERY_CHOICES = [
        ('retrait', 'Retrait au magasin'),
        ('livraison', 'Livraison'),
    ]

    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    delivery_method = models.CharField(max_length=20, choices=DELIVERY_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    catalogue = models.ForeignKey(Catalogue, on_delete=models.CASCADE)

    def __str__(self):
        return f"Commande de {self.user.username} : {self.product.name} x{self.quantity}"

