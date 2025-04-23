from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import Product, Order
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
        quantity = int(request.POST.get('quantity'))
        delivery_method = request.POST.get('delivery_method')
        phone_number = request.POST.get('phone_number')  # 🔥 récupération du numéro

        order = Order.objects.create(
            client=request.user,
            product=product,
            quantity=quantity,
            delivery_method=delivery_method,
            phone_number=phone_number  # 🔥 stockage du numéro
        )

        # Notification Discord (code que je t'avais déjà donné)
        send_discord_notification(order)

        messages.success(request, 'Commande passée avec succès !')
        return redirect('dashboard')
    return render(request, 'place_order.html', {'product': product})


def send_discord_notification(order):
    if order.product.catalogue == 1:
        webhook_url = settings.DISCORD_LEGAL_WEBHOOK
        mention = "@TroTro"
        catalogue_name = "Catalogue Légal"
    elif order.product.catalogue == 2:
        webhook_url = settings.DISCORD_ILLEGAL_WEBHOOK
        mention = "@AladindeAuCurry"
        catalogue_name = "Catalogue Illégal"
    else:
        return  # Pas de webhook si le catalogue est incorrect

    data = {
        "content": f"📦 Nouvelle commande passée par **{order.client.username}** sur **{catalogue_name}**.\n"
                   f"Produit : {order.product.name}\n"
                   f"Quantité : {order.quantity}\n"
                   f"Méthode de livraison : {order.delivery_method}\n"
                   f"Notification : {mention}"
    }

    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code != 204:
            print(f"Erreur lors de l'envoi du message Discord : {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Erreur Discord Webhook : {e}")
