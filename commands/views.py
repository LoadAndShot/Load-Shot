# commands/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Order
from django.conf import settings
import requests

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def catalogue1(request):
    products = Product.objects.filter(catalogue=1)
    return render(request, 'catalogue1.html', {'products': products})

@login_required
def catalogue2(request):
    products = Product.objects.filter(catalogue=2)
    return render(request, 'catalogue2.html', {'products': products})

@login_required
def place_order(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        delivery_method = request.POST.get('delivery_method')
        phone_number = request.POST.get('phone_number', '')

        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            delivery_method=delivery_method,
            phone_number=phone_number
        )

        # Envoi de la notif Discord
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
