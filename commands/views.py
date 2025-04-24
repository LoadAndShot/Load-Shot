from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Order
from bot.bot import send_order_notification

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
def remove_from_cart(request, index):
    cart = request.session.get('cart', [])
    
    try:
        removed_item = cart.pop(index)
        request.session['cart'] = cart  # Update le panier après suppression
        messages.success(request, f"Produit '{removed_item['product_name']}' retiré du panier.")
    except IndexError:
        messages.error(request, "Produit introuvable dans le panier.")

    return redirect('view_cart')


@login_required
def confirm_order(request):
    cart = request.session.get('cart', [])
    if not cart:
        messages.error(request, "Votre panier est vide.")
        return redirect('dashboard')

    total_price = sum(item['quantity'] * item['price'] for item in cart)

    if request.method == 'POST':
        for item in cart:
            product = get_object_or_404(Product, id=item['product_id'])
            Order.objects.create(
                user=request.user,
                product=product,
                quantity=item['quantity'],
                phone_number=item['phone_number'],
                delivery_method=item['delivery_method'],
                is_delivered=False
            )
        send_order_notification(request.user.username, cart, total_price)
        request.session['cart'] = []
        messages.success(request, "Commande confirmée et envoyée !")
        return redirect('dashboard')

    return render(request, 'confirm_order.html', {'cart': cart, 'total_price': total_price})

