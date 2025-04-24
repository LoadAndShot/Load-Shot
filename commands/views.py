from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Order
from django.contrib.auth.decorators import login_required
from django.conf import settings
import requests

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
