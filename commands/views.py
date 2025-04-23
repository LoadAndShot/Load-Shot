from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Order
import requests
import os

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
        delivery_method = request.POST.get('delivery_method')
        quantity = int(request.POST.get('quantity'))
        order = Order.objects.create(
            client=request.user,
            product=product,
            quantity=quantity,
            delivery_method=delivery_method
        )
        messages.success(request, 'Commande passée avec succès !')
        
        # Envoi de la notification Discord
        send_discord_notification(order)

        return redirect('dashboard')
    return render(request, 'place_order.html', {'product': product})

def send_discord_notification(order):
    catalogue = order.product.catalogue
    webhook_url = None
    mention = None

    if catalogue == 1:
        webhook_url = os.getenv('DISCORD_LEGAL_WEBHOOK')
        mention = "@TroTro"
    elif catalogue == 2:
        webhook_url = os.getenv('DISCORD_ILLEGAL_WEBHOOK')
        mention = "@AladindeAuCurry"

    if webhook_url:
        message = f"Nouvelle commande de **{order.client.username}** : {order.quantity}x {order.product.name} par {order.delivery_method}. {mention}"
        payload = {"content": message}
        requests.post(webhook_url, json=payload)
