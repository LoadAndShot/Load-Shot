from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from django.contrib import messages
from bot.bot import send_order_notification

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        quantity = int(request.POST['quantity'])
        delivery_method = request.POST['delivery_method']
        phone_number = request.POST['phone_number']

        cart = request.session.get('cart', [])
        cart.append({
            'product_id': product.id,
            'product_name': product.name,
            'quantity': quantity,
            'price': float(product.price),
            'delivery_method': delivery_method,
            'phone_number': phone_number
        })
        request.session['cart'] = cart
        messages.success(request, f"{product.name} ajouté au panier.")
        return redirect('dashboard')

    return render(request, 'add_to_cart.html', {'product': product})

@login_required
def view_cart(request):
    cart = request.session.get('cart', [])
    total_price = sum(item['quantity'] * item['price'] for item in cart)
    return render(request, 'cart.html', {'cart': cart, 'total_price': total_price})

@login_required
def confirm_order(request):
    cart = request.session.get('cart', [])
    if not cart:
        messages.error(request, "Votre panier est vide.")
        return redirect('dashboard')
        from django.shortcuts import render

def dashboard(request):
    return render(request, 'dashboard.html'

    if request.method == 'POST':
        total_price = sum(item['quantity'] * item['price'] for item in cart)
        for item in cart:
            product = get_object_or_404(Product, id=item['product_id'])
            Order.objects.create(
                user=request.user,
                product=product,
                quantity=item['quantity'],
                phone_number=item['phone_number'],
                is_delivered=False
            )
        send_order_notification(request.user.username, cart, total_price)
        request.session['cart'] = []
        messages.success(request, "Commande confirmée et envoyée !")
        return redirect('dashboard')

    total_price = sum(item['quantity'] * item['price'] for item in cart)
    return render(request, 'confirm_order.html', {'cart': cart, 'total_price': total_price})
