from django.db import models
from django.conf import settings  # 🔥 Pour utiliser AUTH_USER_MODEL

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    catalog = models.IntegerField(choices=[(1, 'Catalogue 1'), (2, 'Catalogue 2')])  # Pas 'catalogue' mais 'catalog'

    def __str__(self):
        return self.name

class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # 🔥 Correct ici
    quantity = models.IntegerField(default=1)
    delivery_method = models.CharField(max_length=50, choices=[('pickup', 'Retrait'), ('delivery', 'Livraison')])  # Ajouté car manquant
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.client.username}"
