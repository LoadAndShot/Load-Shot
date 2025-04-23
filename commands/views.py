# commands/views.py

from django.shortcuts import render, redirect, get_object_or_404
# commands/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Order
from django.conf import settings
import requests

@login_required
def dashboard(request):
    catalogue1 = Product.objects.filter(catalogue=1)
    catalogue2 = Product.objects.filter(catalogue=2)
    return render(request, 'dashboard.html', {
        'catalogue1': catalogue1,
        'catalogue2': catalogue2,
    })

@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        delivery_method = request.POST.get('delivery_method')  # <- correction ici
        phone_number = request.POST.get('phone_number', '')

        # Création de la commande avec 'user', 'delivery_method', et 'phone_number'
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            delivery_method=delivery_method,  # <- correction ici
            phone_number=phone_number
        )

        # Notification Discord
        if product.catalogue == 1:
            webhook_url = settings.DISCORD_LEGAL_WEBHOOK
            mention = "@TroTro"
        else:
            webhook_url = settings.DISCORD_ILLEGAL_WEBHOOK
            mention = "@AladindeAuCurry"

        data = {
            "content": f"{mention} Nouvelle commande : {order.quantity} x {order.product.name} par {order.user.username} (Tel IG : {order.phone_number}) - Livraison : {order.delivery_method}"
        }
        try:
            requests.post(webhook_url, json=data)
        except Exception as e:
            messages.error(request, f"Erreur d'envoi Discord : {e}")

        messages.success(request, "Commande passée avec succès !")
        return redirect('dashboard')

    return render(request, 'place_order.html', {'product': product})
