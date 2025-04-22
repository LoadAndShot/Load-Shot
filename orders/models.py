from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_legal = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Order(models.Model):
    DELIVERY_CHOICES = (
        ('RETRAIT', 'Retrait magasin'),
        ('LIVRAISON', 'Livraison'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField()
    is_illegal = models.BooleanField(default=False)
    delivery_method = models.CharField(max_length=10, choices=DELIVERY_CHOICES)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Commande de {self.user.username} - {self.product.name if self.product else 'Pas de produit'}"

