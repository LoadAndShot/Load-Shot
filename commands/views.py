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
    @login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    delivery_method = request.POST.get('delivery_method')
    phone_number = request.POST.get('phone_number')

    cart = request.session.get('cart', [])

    cart.append({
        'product_id': product.id,
        'product_name': product.name,
        'price': float(product.price),
        'quantity': quantity,
        'delivery_method': delivery_method,
        'phone_number': phone_number,
    })

    request.session['cart'] = cart
    return redirect('cart_summary')

@login_required
def cart_summary(request):
    cart = request.session.get('cart', [])
    total_price = sum(item['price'] * item['quantity'] for item in cart)
    return render(request, 'cart_summary.html', {'cart': cart, 'total_price': total_price})

@login_required
def validate_cart(request):
    cart = request.session.get('cart', [])
    if not cart:
        return redirect('dashboard')

    total_price = sum(item['price'] * item['quantity'] for item in cart)
    for item in cart:
        product = Product.objects.get(id=item['product_id'])
        Order.objects.create(
            user=request.user,
            product=product,
            quantity=item['quantity'],
            phone_number=item['phone_number'],
            is_delivered=False,
            delivery_method=item['delivery_method']
        )

    # Discord Notification
    webhook_url = settings.DISCORD_WEBHOOK_LEGAL if all(p['delivery_method'] == 'livraison' for p in cart) else settings.DISCORD_WEBHOOK_ILLEGAL
    message = f"Nouvelle commande par {request.user.username} - Prix total : {total_price}€"
    requests.post(webhook_url, json={"content": message})

    request.session['cart'] = []  # Clear cart after order
    return redirect('dashboard')
