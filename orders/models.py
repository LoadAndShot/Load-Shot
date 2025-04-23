from django.db import models
from django.contrib.auth.models import User

class Order(models.Model):
    # Choix possibles pour le type de produit et la méthode
    TYPE_CHOICES = [
        ('legal', 'Légal'),
        ('illegal', 'Illégal'),
    ]
    METHOD_CHOICES = [
        ('pickup', 'Retrait'),
        ('delivery', 'Livraison'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    product_type = models.CharField("Type de produit", max_length=20, choices=TYPE_CHOICES)
    method = models.CharField("Méthode", max_length=20, choices=METHOD_CHOICES)
    created_at = models.DateTimeField("Date de création", auto_now_add=True)
    sent_to_discord = models.BooleanField("Envoyé sur Discord", default=False)  # statut d'envoi au bot Discord

    def __str__(self):
        return f"Commande #{self.id} - {self.get_product_type_display()} - {self.get_method_display()}"
