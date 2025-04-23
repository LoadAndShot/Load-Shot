from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    catalogue = models.PositiveSmallIntegerField(choices=[(1, 'Catalogue 1'), (2, 'Catalogue 2')])

    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    delivery_method = models.CharField(max_length=100, choices=[('pickup', 'Retrait sur place'), ('delivery', 'Livraison')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande de {self.client.username} - {self.product.name}"
