from django.contrib import admin
from .models import Order

# Configuration de l'affichage du modèle Order dans l'interface d'administration
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_type', 'method', 'created_at', 'sent_to_discord')
    list_filter = ('product_type', 'method', 'sent_to_discord')
    search_fields = ('user__username',)
