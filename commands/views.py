from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from bot.bot import send_order_notification

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    cart = request.session.get('cart', [])
    quantity = int(request.POST.get('quantity', 1))
    delivery_method = request.POST.get('delivery_method')
    phone_number = request.POST.get('phone_number')

    cart.append({
        'product_id': product.id,
        'product_name': product.name,
        'price': float(product.price),
        'quantity': quantity,
        'delivery_method': delivery_method,
        'phone_number': phone_number,
    })

    request.session['cart'] = cart
    messages.success(request, f"{product.name} ajouté au panier.")
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = request.session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    return render(request, 'cart.html', {'cart': cart, 'total': total})

@login_required
def validate_cart(request):
    cart = request.session.get('cart', [])
    if not cart:
        messages.error(request, "Votre panier est vide.")
        return redirect('dashboard')

    for item in cart:
        product = Product.objects.get(id=item['product_id'])
        Order.objects.create(
            user=request.user,
            product=product,
            quantity=item['quantity'],
            phone_number=item['phone_number'],
            delivery_method=item['delivery_method']
        )

    total = sum(item['price'] * item['quantity'] for item in cart)
    send_order_notification(request.user.username, cart, total)
    request.session['cart'] = []  # Vide le panier après validation

    messages.success(request, "Commande validée et envoyée.")
    return redirect('dashboard')
