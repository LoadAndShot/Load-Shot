# commands/models.py

from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    catalogue = models.IntegerField()  # 1 = légal, 2 = illégal

    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    delivery_method = models.CharField(max_length=20, choices=[('livraison', 'Livraison'), ('retrait', 'Retrait')])
    phone_number = models.CharField(max_length=50)  # ✅ Ici tu ajoutes le numéro de téléphone IG
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande de {self.product.name} par {self.client.username}"
