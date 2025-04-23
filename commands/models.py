from django.db import models
from django.conf import settings

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    catalogue = models.IntegerField(choices=[(1, 'Catalogue 1'), (2, 'Catalogue 2')])

    def __str__(self):
        return self.name

class Order(models.Model):
    client = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    delivery_method = models.CharField(max_length=50, choices=[('Retrait', 'Retrait'), ('Livraison', 'Livraison')])
    created_at = models.DateTimeField(auto_now_add=True)
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return f"Commande de {self.client.username} - {self.product.name}"
